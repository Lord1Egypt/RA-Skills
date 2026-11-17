#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""invoice_forward.py — 邮箱发票自动转发（配置驱动，无人值守）

流程：IMAP 扫描收件箱主题含关键词的邮件 → 下载发票附件（PDF/OFD/XML）解析 →
     命中抬头规则（默认全部）→ SMTP 标准化转发（主题/正文模板 + 原始发票文件）。

子命令：
  setup                一次性配置：交互/命令行收集配置与授权码，验证连通性后写入
                      config.json + secrets（chmod 600），省去手动改文件
  check                体检：配置 / 凭证 / 依赖 / IMAP / SMTP 逐项验证（setup 后必跑）
  scan  [--days N]     干跑预览：列出候选、解析结果、将执行的动作（不发送、不写状态）
  run   [--days N]     正式执行：转发命中发票 + 写去重状态 + 生成报告
  parse <发票文件>     调试：查看单个发票（PDF/OFD/XML）的字段提取结果

配置：默认 ~/.workbuddy/invoice-forward/config.json（--config 或环境变量
      INVOICE_FORWARD_CONFIG 覆盖）。模板见 references/config.example.json。
凭证：授权码存独立 secrets 文件（默认 ~/.workbuddy/secrets/invoice-forward.env，
      chmod 600），字段 MAIL_USER / MAIL_AUTH_CODE。绝不写入 config 或 skill 包。
去重：state 文件按 Message-ID + 发票号双重去重（QQ 邮箱 IMAP UID 跨会话会重排，
      不可用 UID/序号做去重键）。
依赖：PDF 解析需 pdfplumber（主，视觉顺序提取）或 pymupdf/fitz（兜底）至少其一；OFD/XML 用 Python 内置 zipfile + xml.etree，无需额外安装。
"""
import argparse
import collections
import copy
import datetime
import getpass
import html
import imaplib
import ipaddress
import json
import os
import random
import re
import smtplib
import sys
import time
import urllib.parse
import urllib.request
from email import message_from_bytes
from email.header import Header, decode_header, make_header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

__version__ = "1.0.10"

DEFAULT_CONFIG_PATH = os.path.expanduser("~/.workbuddy/invoice-forward/config.json")
DEFAULTS = {
    "account": {
        "imap_host": "imap.qq.com", "imap_port": 993,
        "smtp_host": "smtp.qq.com", "smtp_port": 465,
        "secrets_file": "~/.workbuddy/secrets/invoice-forward.env",
    },
    "scan": {
        "days": 7,
        "subject_keywords": ["发票"],
        "folder": "INBOX",
        # 链接型发票（如腾讯云电子发票邮件里只有下载链接、无 PDF 附件）：
        # 扫描正文链接并下载 PDF。仅接受最终响应确为 PDF 的链接（防误下载）。
        "fetch_links": True,        # 是否启用链接抓取
        "link_domains": [],         # 非空时仅下载这些域名后缀的链接（如 ["myqcloud.com","tencent.com"]）；空=全部
        "link_timeout": 30,         # 单链接下载超时（秒）
        "link_max_bytes": 26214400, # 单链接最大下载字节（25MB，防超限）
        "link_user_agent": "Mozilla/5.0 (compatible; invoice-forward/1.0)",
    },
    "rule": {"buyer_whitelist": []},
    "forward": {
        "to": [],
        "cc": [],
        "subject_tpl": "{item} {amount} {date}",
        "body_tpl": "发票号码：{invoice_no}\n开票日期：{date}\n购买方（抬头）：{buyer}\n"
                    "销售方：{seller}\n物品：{item}\n价税合计：{amount}",
    },
    "state_file": "~/.workbuddy/invoice-forward/processed.json",
    "send": {
        "_comment": "发送节奏（防反垃圾风控）。interval=每封最小间隔秒；jitter=额外随机秒上限；batch_limit=单批最多发送封数(0=不限)。163/126 等严格风控邮箱建议 interval>=3。",
        "interval": 0,
        "jitter": 0,
        "batch_limit": 0,
    },
}


# ---------- 邮箱服务商标识（provider preset）----------
# 仅指定 provider 即可自动填入对应 IMAP/SMTP 主机与端口，免去手动查 host。
# 支持名称（163/126/qq）或完整域名（163.com / mail.126.com 等）。
_PROVIDER_HOSTS = {
    "qq":      ("imap.qq.com", 993, "smtp.qq.com", 465),
    "foxmail": ("imap.qq.com", 993, "smtp.qq.com", 465),
    "163":     ("imap.163.com", 993, "smtp.163.com", 465),
    "126":     ("imap.126.com", 993, "smtp.126.com", 465),
    "yeah":    ("imap.yeah.net", 993, "smtp.yeah.net", 465),
}
# 域名（含子域）后缀 → provider 名
_DOMAIN_TO_PROVIDER = {
    "qq.com": "qq", "foxmail.com": "foxmail",
    "163.com": "163", "126.com": "126", "yeah.net": "yeah",
}
PROVIDER_PRESETS = _PROVIDER_HOSTS  # 保持原名，供潜在调用


def resolve_provider(acc):
    """若配置指定 provider，用预设覆盖 imap/smtp host/port；否则保留显式 host。"""
    prov = (acc.get("provider") or "").strip().lower()
    if not prov:
        return acc
    preset = _PROVIDER_HOSTS.get(prov)
    if preset is None:
        # 也允许直接写完整域名（如 163.com / mail.126.com）
        dom = prov.split("@")[-1]
        key = _DOMAIN_TO_PROVIDER.get(dom) or _DOMAIN_TO_PROVIDER.get(dom.split(".", 1)[-1])
        if key:
            preset = _PROVIDER_HOSTS[key]
    if preset:
        acc["imap_host"], acc["imap_port"], acc["smtp_host"], acc["smtp_port"] = preset
    else:
        sys.stderr.write("警告：未知的 provider=%r，将使用配置中的 imap_host/smtp_host\n" % prov)
    return acc


# ---------- 配置与凭证 ----------

def _merge(base, override):
    out = dict(base)
    for k, v in (override or {}).items():
        out[k] = _merge(base[k], v) if isinstance(v, dict) and isinstance(base.get(k), dict) else v
    return out


def load_config(path):
    if not os.path.exists(path):
        sys.exit("未找到配置文件 %s\n参照 references/config.example.json 创建，"
                 "或让 WorkBuddy 按 SKILL.md 的 setup 流程引导生成。" % path)
    try:
        cfg = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        sys.exit("配置文件 JSON 解析失败：%s" % e)
    cfg = _merge(DEFAULTS, cfg)
    resolve_provider(cfg["account"])
    return cfg, path


def load_cred(secrets_path):
    # 优先环境变量：临时隔离验证 / CI / 容器场景用，避免授权码落盘。
    # 仅当 MAIL_USER 与 MAIL_AUTH_CODE 同时存在时才走环境变量。
    env_user = (os.environ.get("MAIL_USER") or "").strip()
    env_code = (os.environ.get("MAIL_AUTH_CODE") or "").strip()
    if env_user and env_code:
        return env_user, env_code
    p = os.path.expanduser(secrets_path)
    if not os.path.exists(p):
        sys.exit("未找到凭证文件 %s（需含 MAIL_USER / MAIL_AUTH_CODE，权限 600）" % p)
    try:
        with open(p, encoding="utf-8") as fp:
            kv = dict(l.split("=", 1) for l in fp if "=" in l and not l.startswith("#"))
    except OSError as e:
        sys.exit("凭证文件 %s 读取失败：%s（检查文件权限）" % (p, e))
    user = (kv.get("MAIL_USER") or "").strip()
    code = (kv.get("MAIL_AUTH_CODE") or "").strip()
    if not user or not code:
        sys.exit("凭证文件 %s 缺少 MAIL_USER 或 MAIL_AUTH_CODE" % p)
    return user, code


# ---------- 发票 PDF 解析 ----------

def dhead(s):
    if not s:
        return ""
    try:
        return str(make_header(decode_header(s)))
    except Exception:
        return s


def pdf_text(data: bytes) -> str:
    """pdfplumber 按视觉顺序提取（发票标签和值同行）；fitz 是内容流顺序，
    OFD 转换的发票会把标签和值拆到两个文本块导致正则失配，仅作兜底。"""
    try:
        import io
        import pdfplumber
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            return "\n".join((p.extract_text() or "") for p in pdf.pages)
    except ImportError:
        pass
    except Exception:
        return ""
    try:
        import fitz
        with fitz.open(stream=data, filetype="pdf") as doc:
            return "\n".join(pg.get_text() for pg in doc)
    except Exception:
        return ""


# 在「单位词 / xx.xx 金额 / ¥ / x% 税率」前截断。\b 保护商品名里的套装/批次等词
_UNIT = r"(?:台|个|件|份|本|张|套|箱|袋|瓶|只|副|双|次|项|批|组)"
_CUT = re.compile(r"\s+(?=" + _UNIT + r"\b|\d+\.\d{2}\b|[¥￥]|\d+(?:\.\d+)?%)")
# 商品名续行排除：表头/金额/合计类行
_BAD = re.compile(r"项目名称|价税|备注|开票人|合计|规格|税额|税率|\d+\.\d{2}|[¥￥]")


def extract(text: str) -> dict:
    """从发票全文提取转发所需字段。"""
    f = {"item": "", "amount": "", "date": "", "invoice_no": "", "seller": "", "buyer": ""}
    m = re.search(r"名称[:：]\s*([^\s]+)", text)          # 购买方名称（购/销同模板，第一个）
    if m:
        f["buyer"] = m.group(1)
    m = re.search(r"销售方\s*名称[:：]\s*([^\s]+)", text)     # 销售方名称
    if m:
        f["seller"] = m.group(1)
    else:
        # 数电票把购销双方排在同一行（"购 名称:A 售 名称:B"），"销售方 名称" 正则失配，
        # 用「名称:」第 2 次命中兜底（第 1 次已是购买方）。
        names = re.findall(r"名称[:：]\s*([^\s]+)", text)
        if len(names) >= 2:
            f["seller"] = names[1]
    lines = text.split("\n")
    for i, l in enumerate(lines):
        m = re.search(r"\*[^*\n]+\*\s*(.+)", l)           # *税收分类*商品名 行
        if m:
            item = _CUT.split(m.group(1).strip(), maxsplit=1)[0].strip()
            nl = lines[i + 1].strip() if i + 1 < len(lines) else ""  # 型号常折到下一行
            if nl and not _BAD.search(nl) and len(nl) <= 30:
                item = (item + " " + nl).strip()
            f["item"] = item
            break
    m = re.search(r"（小写）\s*[¥￥]?\s*([\d,]+\.\d{2})", text)
    if m:
        f["amount"] = m.group(1).replace(",", "")
    m = re.search(r"开票日期[:：]\s*(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)", text)
    if m:
        f["date"] = re.sub(r"\s+", "", m.group(1))
    m = re.search(r"发票号码[:：]\s*(\d{12,30})", text)
    if m:
        f["invoice_no"] = m.group(1)
    return f


# ---------- 发票格式识别（PDF / OFD / XML）----------
INVOICE_SUFFIX = {".pdf": "pdf", ".ofd": "ofd", ".xml": "xml"}


def detect_fmt_from_name(fn):
    low = (fn or "").lower()
    for suf, fmt in INVOICE_SUFFIX.items():
        if low.endswith(suf):
            return fmt
    return ""


def _looks_like_ofd(data):
    """OFD 本质是 ZIP 容器，根目录含 OFD.xml；用此区分普通 zip 与发票 OFD。"""
    try:
        import io, zipfile
        z = zipfile.ZipFile(io.BytesIO(data))
    except Exception:
        return False
    return "OFD.XML" in {n.upper() for n in z.namelist()}


_HTML_HEAD = (b"<!doctype", b"<html", b"<head", b"<body", b"<table", b"<div")


def _looks_like_html(data):
    """正文 HTML 也以 '<' 开头。不区分开就会把邮件正文当发票（历史静默漏发的根因）。"""
    head = data[:512].lstrip().lower()
    if any(head.startswith(h) for h in _HTML_HEAD):
        return True
    return b"<html" in head or b"<body" in head


def _looks_like_invoice_xml(data):
    """XML 必须真能解析，且根标签与发票相关；仅「首字符是 <」不足以判定。"""
    if _looks_like_html(data):
        return False
    try:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(data)
    except Exception:
        return False
    tag = (root.tag or "").lower()
    return any(k in tag for k in ("invoice", "einvoice", "发票"))


def detect_fmt_from_magic(data):
    if data[:4] == b"%PDF":
        return "pdf"
    if data[:4] in (b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08"):
        return "ofd" if _looks_like_ofd(data) else ""
    if _looks_like_invoice_xml(data):
        return "xml"
    return ""


_ATTACH_PRIORITY = {"pdf": 0, "ofd": 1, "xml": 2}


def _is_attachment_part(part):
    """只认真正的附件分区：有文件名，或显式声明 attachment。
    邮件正文（text/html、text/plain 且无文件名）必须排除在外。"""
    if dhead(part.get_filename() or ""):
        return True
    return (part.get_content_disposition() or "") == "attachment"


def find_invoice_attachment(msg):
    """在 MIME 树里找发票附件（PDF/OFD/XML）：文件名 / content-type / 魔数三重判定。
    多个候选按 PDF > OFD > XML 取最优（转发只带 PDF，PDF 版面也最贴近视觉顺序）。
    返回 (bytes, filename, fmt)。"""
    best = None
    for part in msg.walk():
        if not _is_attachment_part(part):
            continue
        payload = part.get_payload(decode=True) or b""
        if not payload:
            continue
        fn = dhead(part.get_filename() or "")
        fmt = detect_fmt_from_name(fn)
        if not fmt:
            ct = part.get_content_type().lower()
            if "pdf" in ct:
                fmt = "pdf"
            elif "ofd" in ct:
                fmt = "ofd"
            elif "xml" in ct:
                fmt = "xml"
        if fmt == "xml" and _looks_like_html(payload):
            continue  # 名为 .xml 实为 HTML 的附件（部分服务商正文即附件）
        if not fmt:
            fmt = detect_fmt_from_magic(payload)
        if not fmt:
            continue
        key = _ATTACH_PRIORITY.get(fmt, 9)
        if best is None or key < best[0]:
            best = (key, payload, fn or ("invoice." + fmt), fmt)
    if best:
        return best[1], best[2], best[3]
    return b"", "", ""


def ofd_text(data):
    """从 OFD（ZIP 容器）抽取页面文本：遍历 Pages 下的 Content.xml，
    收集所有 TextCode 元素的文本（按文件顺序）。文本结构接近 PDF 视觉顺序，
    可复用 extract() 正则；抽取不足时上游 extract_invoice 会回退到结构化解析。"""
    try:
        import io, zipfile
        import xml.etree.ElementTree as ET
        z = zipfile.ZipFile(io.BytesIO(data))
    except Exception:
        return ""
    out = []
    page_entries = sorted(n for n in z.namelist()
                          if n.lower().endswith(".xml") and "content" in n.lower())
    for name in page_entries:
        try:
            root = ET.fromstring(z.read(name))
        except Exception:
            continue
        for el in root.iter():
            if el.tag.split('}')[-1].lower() == "textcode":
                txt = "".join(el.itertext()).strip()
                if txt:
                    out.append(txt)
    return "\n".join(out)


def _norm_xml_date(s):
    if not s:
        return ""
    m = re.search(r"(\d{4})[^\d]*(\d{1,2})[^\d]*(\d{1,2})", s)
    if m:
        return "%04d%02d%02d" % (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return s.strip()


def extract_xml(data):
    """从结构化发票 XML（增值税电子发票 FPML / 全电发票等）提取字段。
    命名空间无关：按已知字段标签（大小写不敏感）在全树 / 父子关系中取值。"""
    import xml.etree.ElementTree as ET
    f = {k: "" for k in ("item", "amount", "date", "invoice_no", "seller", "buyer")}
    try:
        root = ET.fromstring(data)
    except Exception:
        return f

    def _all(tag, parent=None):
        tag = tag.lower()
        src = (parent if parent is not None else root).iter()
        return [el for el in src if el.tag.split('}')[-1].lower() == tag]

    def _text(tag, parent=None):
        for el in _all(tag, parent):
            t = "".join(el.itertext()).strip()
            if t:
                return t
        return ""

    f["invoice_no"] = (_text("fphm") or _text("invoiceno") or _text("invoicenumber")
                       or _text("invoicecode"))
    f["date"] = _norm_xml_date(_text("kprq") or _text("invoicedate"))
    gmf = _all("gmf") or _all("buyer")
    gp = gmf[0] if gmf else None
    f["buyer"] = (_text("nsrmc", gp) or _text("gmfmc", gp) or _text("buyername", gp)
                 or _text("gmfnsrmc", gp) or _text("buyername") or _text("gmfmc"))
    xhf = _all("xhf") or _all("seller")
    xp = xhf[0] if xhf else None
    f["seller"] = (_text("nsrmc", xp) or _text("xhfmc", xp) or _text("sellername", xp)
                  or _text("xhfnsrmc", xp) or _text("sellername") or _text("xhfmc"))
    sp = _all("sp") or _all("spxx")
    spp = sp[0] if sp else None
    f["item"] = (_text("xmmc", spp) or _text("itemname", spp) or _text("spmc", spp)
                 or _text("xmmc") or _text("itemname") or _text("spmc"))
    f["amount"] = (_text("jshj") or _text("totalamountwithtax") or _text("hjje")
                   or _text("jshjje") or _text("amount") or _text("totalamount"))
    f["amount"] = f["amount"].replace(",", "")
    return f


def ofd_structured(data):
    """OFD 内若内嵌了结构化发票 XML（部分税务 OFD 会在内部放 FPML/发票.xml），
    优先用结构化解析拿字段，比 TextCode 正则更准；找不到则返回 None。"""
    try:
        import io, zipfile
        import xml.etree.ElementTree as ET
        z = zipfile.ZipFile(io.BytesIO(data))
    except Exception:
        return None
    for name in z.namelist():
        if not name.lower().endswith(".xml"):
            continue
        try:
            root = ET.fromstring(z.read(name))
        except Exception:
            continue
        ln = root.tag.split('}')[-1].lower()
        if ln in ("fpml", "invoice", "einvoice") or "invoice" in name.lower():
            sf = extract_xml(z.read(name))
            if sf.get("invoice_no") or sf.get("buyer"):
                return sf
    return None


def xml_flat_text(data):
    """XML 全文文本（供抬头全文本兜底匹配用）。"""
    import xml.etree.ElementTree as ET
    try:
        root = ET.fromstring(data)
    except Exception:
        return ""
    return "\n".join(t for t in ("".join(el.itertext()).strip() for el in root.iter()) if t)


def extract_invoice(data, fmt):
    """按格式提取转发字段，返回 (fields, text)。
    PDF 抽文本后走正则；OFD 先抽 TextCode 文本走正则，不足则回退内嵌结构化 XML；
    XML 直接走结构化解析（最可靠）。text 用于抬头全文本兜底匹配。"""
    if fmt == "xml":
        return extract_xml(data), xml_flat_text(data)
    if fmt == "ofd":
        t = ofd_text(data)
        f = extract(t)
        if not (f.get("invoice_no") or f.get("buyer")):
            sf = ofd_structured(data)
            if sf and (sf.get("invoice_no") or sf.get("buyer")):
                f = sf
        return f, t
    t = pdf_text(data)
    return extract(t), t


def extract_links(msg):
    """从邮件正文提取 http(s) 链接：HTML 的 href/src + 纯文本 URL。
    HTML 实体反转义（如 &amp; → &），去重。返回唯一链接列表。"""
    raw = []
    for part in msg.walk():
        ct = part.get_content_type()
        if ct == "text/html":
            body = part.get_payload(decode=True) or b""
            try:
                body = body.decode(part.get_content_charset() or "utf-8", "ignore")
            except Exception:
                body = body.decode("utf-8", "ignore")
            raw += re.findall(r'(?:href|src)=["\']([^"\']+)', body, re.I)
        elif ct == "text/plain":
            body = part.get_payload(decode=True) or b""
            try:
                body = body.decode(part.get_content_charset() or "utf-8", "ignore")
            except Exception:
                body = body.decode("utf-8", "ignore")
            raw += re.findall(r'https?://[^\s<>"\']+', body)
    out, seen = [], set()
    for u in raw:
        u = html.unescape(u).strip()
        if u.lower().startswith(("http://", "https://")) and u not in seen:
            seen.add(u)
            out.append(u)
    return out


def _host_is_blocked(host):
    """SSRF 基础防护：仅拒绝「字面量 IP」落在私有/环回/链路本地/保留/多播段。
    不做域名 DNS 解析拦截——解析结果在代理/沙箱环境下不可靠，会误杀合法公有 CDN
    （如腾讯云 COS myqcloud.com）。真正的防线是 download_link_invoice 里「仅接受最终响应
    确为 PDF」的闸门（不执行任何内容，只保存 PDF 字节）。"""
    if not host:
        return True
    if host.startswith("["):  # IPv6 字面量
        host = host.strip("[]").split("%")[0]
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return False  # 域名：放行（靠 PDF 闸门兜底）
    return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast


def _link_filename(disp, p, fmt):
    m = re.search(r'filename\*?=(?:UTF-8\'\')?["\']?([^"\';]+)', disp or "", re.I)
    if m:
        fn = urllib.parse.unquote(m.group(1)).strip()
        if fn.lower().endswith("." + fmt):
            return fn
    base = os.path.basename(p.path.split("?")[0])
    if base.lower().endswith("." + fmt):
        return base
    return "invoice-link." + fmt


def download_link_invoice(url, cfg):
    """下载链接；仅当最终响应确为发票（PDF/OFD/XML）时返回 (bytes, filename, fmt)，
    否则 (b"", "", "")。安全闸门：仅 http(s)；可选域名白名单；SSRF 基础防护；限大小/超时；
    最终内容必须是发票格式（Content-Type / Content-Disposition 后缀 / 魔数）。"""
    scan = cfg.get("scan", {})
    allow = [d.lower() for d in (scan.get("link_domains") or [])]
    timeout = int(scan.get("link_timeout", 30) or 30)
    max_bytes = int(scan.get("link_max_bytes", 26214400) or 26214400)
    ua = scan.get("link_user_agent") or "Mozilla/5.0 (compatible; invoice-forward/1.0)"
    p = urllib.parse.urlparse(url)
    if p.scheme not in ("http", "https") or not p.hostname:
        return b"", "", ""
    if allow and not any(p.hostname.lower().endswith(d) for d in allow):
        return b"", "", ""
    if _host_is_blocked(p.hostname):
        return b"", "", ""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": ua})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            ctype = (r.headers.get("Content-Type") or "").lower()
            disp = r.headers.get("Content-Disposition") or ""
            data = r.read(max_bytes + 1)
            if len(data) > max_bytes:
                return b"", "", ""
            fmt = ""
            if "pdf" in ctype or "pdf" in disp.lower():
                fmt = "pdf"
            elif "ofd" in ctype or ".ofd" in disp.lower():
                fmt = "ofd"
            elif "xml" in ctype or ".xml" in disp.lower():
                fmt = "xml"
            if not fmt:
                fmt = detect_fmt_from_magic(data)
            if not fmt:
                return b"", "", ""
            return data, _link_filename(disp, p, fmt), fmt
    except Exception:
        return b"", "", ""


def fetch_invoice(imap, uid, cfg):
    """取邮件发票：优先附件（PDF/OFD/XML）；无附件则扫描正文链接尝试下载。
    返回 (data, filename, fmt, link_tried)。link_tried=True 表示曾尝试链接下载
    （用于无发票时给出更精确的原因：链接未返回发票文件 / 链接抓取被禁用）。"""
    _, data = imap.uid("FETCH", uid, "(RFC822)")
    msg = message_from_bytes(data[0][1])
    att, fname, fmt = find_invoice_attachment(msg)
    if att:
        return att, fname, fmt, False
    if not cfg.get("scan", {}).get("fetch_links", True):
        return b"", "", "", False
    for url in extract_links(msg):
        att, fname, fmt = download_link_invoice(url, cfg)
        if att:
            return att, fname, fmt, True
    return b"", "", "", True


# ---------- IMAP ----------

def imap_scan(user, code, cfg, days):
    """单连接完成 登录→SINCE 搜索→批量取主题过滤。
    返回 (imap连接, 候选列表[(uid, msgid, subject)], 近 days 天邮件总数)。
    连接保持打开供 imap_fetch_invoice 复用，调用方负责 logout。"""
    acc = cfg["account"]
    imap = imaplib.IMAP4_SSL(acc["imap_host"], acc["imap_port"], timeout=30)
    imap.login(user, code)
    # 网易(163/126)要求先发 IMAP ID 自报身份，否则 SELECT/EXAMINE 返回
    # "Unsafe Login" 并拒绝选文件夹。其他服务器通常支持/忽略 ID，故尽力发送、忽略失败。
    try:
        imap.xatom("ID", '("name" "invoice-forward" "version" "%s")' % __version__)
    except Exception:
        pass
    # 只读 SELECT：163 等邮箱在 "Unsafe Login" 风控下会拒绝读写 SELECT（返回 NO 并留在
    # AUTH 态，导致后续 SEARCH 报 illegal in state AUTH）；扫描只用读（SEARCH/BODY.PEEK），
    # 只读 SELECT 既能绕过该限制，对 QQ 等也无副作用。
    typ, resp = imap.select(cfg["scan"]["folder"], readonly=True)
    if typ != "OK":
        sys.exit("IMAP 选择文件夹 %s 失败：%s（检查文件夹名或邮箱风控设置）"
                 % (cfg["scan"]["folder"], resp))
    since = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%d-%b-%Y")
    # UID SEARCH 条件必须分开传；整串带括号 "(SINCE ...)" 会被 QQ 服务器静默忽略返回全部
    _, data = imap.uid("SEARCH", None, "SINCE", since)
    uids = data[0].split() if data and data[0] else []
    cand = []
    if uids:
        _, data = imap.uid("FETCH", b",".join(uids),
                           "(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM MESSAGE-ID)])")
        kws = cfg["scan"]["subject_keywords"]
        exclude = {a.lower() for a in cfg["forward"]["to"]}  # 防自转发循环
        for part in data:
            if not isinstance(part, tuple):
                continue
            m_uid = re.search(rb"UID (\d+)", part[0])  # 某些服务器可能不带 UID，跳过而非崩溃
            if not m_uid:
                continue
            uid = m_uid.group(1).decode()
            msg = message_from_bytes(part[1])
            subj, frm = dhead(msg.get("Subject")), dhead(msg.get("From"))
            msgid = dhead(msg.get("Message-ID")) or (frm + "|" + subj)
            frm_addr = (re.search(r"[\w.\-]+@[\w.\-]+", frm) or [None])[0]
            if any(k in subj for k in kws) and (frm_addr or "").lower() not in exclude:
                cand.append((uid, msgid, subj))
    return imap, cand, len(uids)


def imap_fetch_invoice(imap, uid):
    """取邮件全量（RFC822）→ 仅首要发票附件（PDF/OFD/XML，不含链接抓取）。供 parse/调试用。"""
    _, data = imap.uid("FETCH", uid, "(RFC822)")
    return find_invoice_attachment(message_from_bytes(data[0][1]))


# ---------- 转发 ----------

def render(tpl, fields):
    """模板渲染，缺失字段渲染为空串而不是报错。"""
    return tpl.format_map(collections.defaultdict(str, fields))


class SmtpSession:
    """惰性建立的单 SMTP 连接，供逐封发送复用。"""

    def __init__(self, user, code, cfg):
        self.user, self.code, self.cfg, self.conn = user, code, cfg, None

    def send(self, subject, body, data, fname, fmt):
        if self.conn is None:
            acc = self.cfg["account"]
            self.conn = smtplib.SMTP_SSL(acc["smtp_host"], acc["smtp_port"], timeout=30)
            self.conn.login(self.user, self.code)
        m = MIMEMultipart()
        m["From"] = self.user
        m["To"] = ", ".join(self.cfg["forward"]["to"])
        cc = self.cfg["forward"].get("cc") or []
        if cc:
            m["Cc"] = ", ".join(cc)
        m["Subject"] = Header(subject, "utf-8")
        m.attach(MIMEText(body, "plain", "utf-8"))
        att = MIMEApplication(data, _subtype=(fmt or "pdf"))
        att.add_header("Content-Disposition", "attachment", filename=("utf-8", "", fname))
        m.attach(att)
        self.conn.send_message(m)

    def close(self):
        if self.conn:
            try:
                self.conn.quit()
            except Exception:
                pass


# ---------- 状态 ----------

def load_state(path):
    p = os.path.expanduser(path)
    if os.path.exists(p):
        try:
            return json.load(open(p, encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_state(path, state):
    p = os.path.expanduser(path)
    try:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fp:
            json.dump(state, fp, ensure_ascii=False, indent=2)
    except OSError as e:
        # 状态写失败必须响亮失败——静默吞掉会导致下次运行重复转发
        sys.exit("状态文件 %s 写入失败：%s（为防重复转发，本次中止）" % (p, e))


def buyer_hit(cfg, fields, text):
    """抬头白名单判定。已提取到购买方时按名称精确比对（允许互为子串，吸收空格差异），
    避免备注栏出现同名公司造成误判；仅当购买方提取失败时才用全文本兜底。"""
    wl = cfg["rule"]["buyer_whitelist"]
    if not wl:
        return True
    buyer = fields.get("buyer", "")
    if buyer:
        return any(name == buyer or name in buyer or buyer in name for name in wl)
    return any(name in text for name in wl)


# ---------- 主流程 ----------

def process(cfg, days, do_send):
    # PDF 解析库仅在遇到 PDF 发票时需要；OFD/XML 用内置 zip+xml 解析，无需第三方库。
    pdf_ok = True
    try:
        import pdfplumber  # noqa
    except ImportError:
        try:
            import fitz  # noqa
        except ImportError:
            pdf_ok = False
            print("[警告] 未安装 PDF 解析库（pdfplumber/pymupdf），遇到 PDF 发票将跳过；"
                  "OFD/XML 不受影响。可跑 check --install-deps 自动安装。")
    user, code = load_cred(cfg["account"]["secrets_file"])
    state = load_state(cfg["state_file"])
    print("[连接] 正在登录 %s 并扫描近 %d 天邮件…" % (cfg["account"]["imap_host"], days))
    imap, cand, total = imap_scan(user, code, cfg, days)
    print("[扫描] 近 %d 天收件箱 %d 封，发票候选 %d 封" % (days, total, len(cand)))

    todo = [(u, k, s) for u, k, s in cand if k not in state]
    print("[待办] 未处理 %d 封（其余 %d 封已去重跳过）" % (len(todo), len(cand) - len(todo)))

    sent, skipped, no_invoice, failed, deferred = [], [], [], [], []
    send_cfg = cfg.get("send", {})
    interval = int(send_cfg.get("interval", 0) or 0)
    jitter = int(send_cfg.get("jitter", 0) or 0)
    batch_limit = int(send_cfg.get("batch_limit", 0) or 0)
    sent_count = 0
    smtp = SmtpSession(user, code, cfg) if do_send else None
    if do_send and (interval or batch_limit):
        print("[节奏] 每封间隔 %ss（±%ss），单批上限 %s 封"
              % (interval, jitter, batch_limit or "无"))
    for idx, (uid, key, subj) in enumerate(todo):
        if batch_limit and sent_count >= batch_limit:
            deferred.append(subj)
            continue
        att, fname, fmt, link_tried = fetch_invoice(imap, uid, cfg)
        if not att:
            reason = ("链接均未返回发票文件（可能需登录或链接已过期）" if link_tried
                      else "链接抓取已禁用")
            no_invoice.append((subj, reason))
            state[key] = {"status": "no_invoice", "subject": subj, "reason": reason}
            continue
        if fmt == "pdf" and not pdf_ok:
            no_invoice.append((subj, "缺少PDF解析库（pdfplumber/pymupdf），请先 check --install-deps"))
            state[key] = {"status": "no_parser", "subject": subj}
            continue
        f, text = extract_invoice(att, fmt)
        # 解析失败必须响亮：购买方没提取到就无法判定抬头，一律进「待人工」，
        # 绝不允许落到 skipped——否则同一分支既表示「抬头不符」又表示「没解析出来」，
        # 报告上看不出漏发（历史事故：正文 HTML 被当发票，4 张全被记成跳过）。
        if cfg["rule"]["buyer_whitelist"] and not (f.get("buyer") or "").strip():
            reason = ("解析失败：未提取到购买方名称（格式 %s，%d 字节），无法判定抬头"
                      % (fmt, len(att)))
            no_invoice.append((subj, reason))
            state[key] = {"status": "parse_failed", "subject": subj, "reason": reason}
            continue
        if not buyer_hit(cfg, f, text):
            skipped.append(subj)
            state[key] = {"status": "skipped", "subject": subj}
            continue
        if f["invoice_no"] and f["invoice_no"] in state.get("_nos", []):
            skipped.append(subj + "（发票号重复）")
            state[key] = {"status": "dup_invoice", "subject": subj}
            continue
        item = f["item"] or re.sub(r"^(转发|Fw)[:：]\s*", "", subj)  # 提取失败回退原主题
        f["item"] = item
        subject = " ".join(render(cfg["forward"]["subject_tpl"], f).split())
        body = render(cfg["forward"]["body_tpl"], f)
        if do_send:
            try:
                smtp.send(subject, body, att, fname, fmt)
            except Exception as e:
                failed.append((subject, str(e)[:100]))  # 不写状态，下轮自动重试
                continue
            sent.append(subject)
            sent_count += 1
            state[key] = {"status": "sent", "subject": subject}
            save_state(cfg["state_file"], state)  # 每发一封即落盘：中途崩溃重跑也不会重发
            # 发送节奏：模拟人类停顿，避免被 163/126 等严格风控判为群发机器人
            more = (idx < len(todo) - 1) and not (batch_limit and sent_count >= batch_limit)
            if interval and more:
                time.sleep(random.uniform(interval, interval + jitter))
        else:
            sent.append(subject + "（预览未发送）")
            sent_count += 1
        if f["invoice_no"]:
            # 同轮内按发票号去重：scan 预览与 run 真实发送必须一致，
            # 否则预览会漏报重复（同一发票被不同邮件多次投递时）。
            state.setdefault("_nos", []).append(f["invoice_no"])
    imap.logout()
    if smtp:
        smtp.close()

    if do_send:
        save_state(cfg["state_file"], state)  # 落盘 skipped/no_invoice/dup 条目

    summary = "[完成] %s %d / 跳过 %d / 无发票待人工 %d%s%s" % (
        "已发送" if do_send else "将发送", len(sent), len(skipped), len(no_invoice),
        " / 发送失败 %d" % len(failed) if failed else "",
        " / 本批上限延后 %d（下轮继续）" % len(deferred) if deferred else "")
    print(summary)
    for s in sent:
        print("  ✅", s)
    for s in skipped:
        print("  ⚪ 跳过:", s)
    for s, reason in no_invoice:
        print("  ⚠️ 无发票:", s, "—", reason)
    for s in deferred:
        print("  ⏸️ 延后:", s)
    for s, err in failed:
        print("  ❌ 发送失败: %s（%s）" % (s, err))

    if do_send:
        now = datetime.datetime.now()
        report = os.path.join(os.path.dirname(os.path.expanduser(cfg["state_file"])),
                              f"报告_{now:%Y%m%d}.md")
        try:
            with open(report, "w", encoding="utf-8") as fp:
                fp.write(f"# 发票转发报告 {now:%Y-%m-%d %H:%M}\n\n- 范围：近 {days} 天；候选 {len(cand)} 封\n- {summary}\n")
                fp.write("\n".join("- ✅ " + s for s in sent))
                fp.write("\n".join("\n- ⚠️ 无发票: %s（%s）" % (s, reason) for s, reason in no_invoice))
                fp.write("\n".join("\n- ⏸️ 延后(本批上限): " + s for s in deferred))
                fp.write("\n".join("\n- ❌ 发送失败: %s（%s）" % (s, err) for s, err in failed))
            print("[报告]", report)
        except OSError as e:
            # 转发本身已成功，报告写失败只告警不中止
            print("[警告] 报告文件写入失败：%s（不影响本次转发结果）" % e)


def _imap_probe(cfg, user, code):
    """登录 IMAP + 发 ID + 只读选文件夹；成功返回封数，失败抛异常。check 与 setup 复用。"""
    acc = cfg["account"]
    m = imaplib.IMAP4_SSL(acc["imap_host"], acc["imap_port"], timeout=15)
    try:
        m.login(user, code)
        try:
            m.xatom("ID", '("name" "invoice-forward" "version" "%s")' % __version__)
        except Exception:
            pass
        typ, d = m.select(cfg["scan"]["folder"], readonly=True)
        if typ != "OK":
            raise RuntimeError("选择文件夹 %s 被拒：%s（邮箱风控/Unsafe Login，请检查 IMAP 服务是否开启）"
                               % (cfg["scan"]["folder"], d))
        return int(d[0].decode())
    finally:
        try:
            m.logout()
        except Exception:
            pass


def _smtp_probe(cfg, user, code):
    """登录 SMTP；成功返回 None，失败抛异常。check 与 setup 复用。"""
    acc = cfg["account"]
    s = smtplib.SMTP_SSL(acc["smtp_host"], acc["smtp_port"], timeout=15)
    try:
        s.login(user, code)
    finally:
        try:
            s.quit()
        except Exception:
            pass


def cmd_check(cfg, install_deps=False):
    ok = True

    def step(name, fn):
        nonlocal ok
        try:
            detail = fn()
            print("✓ %s：%s" % (name, detail or "正常"))
        except Exception as e:
            ok = False
            print("✗ %s：%s" % (name, e))

    step("配置文件", lambda: "已加载")
    step("转发收件人", lambda: ", ".join(cfg["forward"]["to"]) or "未配置！请在 config.json 的 forward.to 填写")
    step("抄送(CC)", lambda: (", ".join(cfg["forward"].get("cc") or []) or "未启用（默认关闭）"))

    def _deps():
        try:
            import pdfplumber  # noqa
            return "pdfplumber 可用（首选）"
        except ImportError:
            pass
        try:
            import fitz  # noqa
            return "仅 fitz 可用（pdfplumber 缺失，建议：pip install pdfplumber）"
        except ImportError:
            pass
        if not install_deps:
            raise RuntimeError("缺少 pdfplumber/pymupdf；重跑 check --install-deps 可自动安装到当前 Python 环境")
        import subprocess
        print("  … 正在自动安装 pdfplumber pymupdf（pip，当前 Python 环境）")
        try:
            r = subprocess.run([sys.executable, "-m", "pip", "install", "pdfplumber", "pymupdf"],
                               capture_output=True, text=True, timeout=600)
        except Exception as e:
            raise RuntimeError("自动安装执行异常（pip 不可用或超时）：%s" % e)
        if r.returncode != 0:
            raise RuntimeError("自动安装失败：" + (r.stderr or r.stdout)[-300:])
        import importlib
        importlib.invalidate_caches()
        import pdfplumber  # noqa
        return "已自动安装 pdfplumber + pymupdf"
    step("PDF 解析依赖（OFD/XML 无需额外库）", _deps)
    user, code = None, None

    def _cred():
        nonlocal user, code
        user, code = load_cred(cfg["account"]["secrets_file"])
        return "%s（授权码已读取）" % user
    step("凭证文件", _cred)

    def _imap():
        return "登录成功，%s 共 %d 封" % (cfg["scan"]["folder"], _imap_probe(cfg, user, code))
    step("IMAP 登录", _imap)

    def _smtp():
        _smtp_probe(cfg, user, code)
        return "登录成功"
    step("SMTP 登录", _smtp)

    print("\n%s" % ("体检通过，可以执行 scan 预览 / run 正式转发" if ok
                    else "体检未通过，请按上面 ✗ 项修复后重跑 check"))
    sys.exit(0 if ok else 1)


def _read_existing_cred(secrets_path):
    """读取已有 secrets 文件，返回 (user, code) 或 (None, None)；不报错、不退出。"""
    p = os.path.expanduser(secrets_path)
    if not os.path.exists(p):
        return None, None
    try:
        with open(p, encoding="utf-8") as fp:
            kv = dict(l.split("=", 1) for l in fp if "=" in l and not l.startswith("#"))
        return (kv.get("MAIL_USER", "").strip() or None,
                kv.get("MAIL_AUTH_CODE", "").strip() or None)
    except OSError:
        return None, None


def _prompt(label, default=None, secret=False):
    """交互询问；非 tty（如 agent 批处理）直接返回 default，缺失由后续校验报错。"""
    if not sys.stdin.isatty():
        return default
    suffix = (" [%s]" % default) if default else ""
    try:
        if secret:
            v = getpass.getpass(label + suffix + "：") or ""
        else:
            v = input(label + suffix + "：").strip()
    except EOFError:
        return default
    return v or (default or "")


def _is_email(s):
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", s or ""))


def _write_config_only(cfg, cfg_path):
    """写入 config.json，剔除任何可能混入的凭证字段，确保结构干净（不含授权码）。"""
    c = copy.deepcopy(cfg)
    for bad in ("user", "auth_code", "MAIL_USER", "MAIL_AUTH_CODE"):
        c.get("account", {}).pop(bad, None)
        c.pop(bad, None)
    os.makedirs(os.path.dirname(cfg_path), exist_ok=True)
    try:
        with open(cfg_path, "w", encoding="utf-8") as fp:
            json.dump(c, fp, ensure_ascii=False, indent=2)
            fp.write("\n")
    except OSError as e:
        sys.exit("配置写入失败 %s：%s（检查目录权限）" % (cfg_path, e))
    print("[setup] 已写入 config.json：%s" % cfg_path)


def _write_secrets(secrets_path, user, code):
    p = os.path.expanduser(secrets_path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    data = "MAIL_USER=%s\nMAIL_AUTH_CODE=%s\n" % (user, code)
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        os.write(fd, data.encode("utf-8"))
    finally:
        os.close(fd)
    try:
        os.chmod(p, 0o600)
    except OSError:
        pass
    print("[setup] 已写入 secrets（权限 600）：%s" % p)


def cmd_setup(args):
    """一次性配置：合并已有 config → 应用 CLI → 交互补缺失 → 验证连通性 → 写盘。"""
    # 1) 基础 = DEFAULTS；已有 config 则合并，避免覆盖既有设置
    cfg = copy.deepcopy(DEFAULTS)
    cfg_path = os.path.abspath(os.path.expanduser(args.config))
    if os.path.exists(cfg_path):
        try:
            cfg = _merge(cfg, json.load(open(cfg_path, encoding="utf-8")))
            print("[setup] 检测到已有配置 %s，将在此基础上合并" % cfg_path)
        except Exception as e:
            print("[setup] 警告：读取已有配置失败（%s），将新建" % e)

    acc = cfg["account"]
    # 2) 应用 CLI 传入的非凭证配置
    if args.provider:
        acc["provider"] = args.provider
    if args.imap_host:
        acc["imap_host"] = args.imap_host
    if args.smtp_host:
        acc["smtp_host"] = args.smtp_host
    if args.imap_port:
        acc["imap_port"] = args.imap_port
    if args.smtp_port:
        acc["smtp_port"] = args.smtp_port
    if args.folder:
        cfg["scan"]["folder"] = args.folder
    if args.days is not None:
        cfg["scan"]["days"] = args.days
    if args.subject_keywords:
        cfg["scan"]["subject_keywords"] = args.subject_keywords
    if args.buyer_whitelist is not None:
        cfg["rule"]["buyer_whitelist"] = args.buyer_whitelist
    if args.to:
        cfg["forward"]["to"] = args.to
    if args.subject_tpl:
        cfg["forward"]["subject_tpl"] = args.subject_tpl
    if args.body_tpl:
        cfg["forward"]["body_tpl"] = args.body_tpl
    if args.interval is not None:
        cfg["send"]["interval"] = args.interval
    if args.jitter is not None:
        cfg["send"]["jitter"] = args.jitter
    if args.batch_limit is not None:
        cfg["send"]["batch_limit"] = args.batch_limit
    if args.fetch_links is not None:
        cfg["scan"]["fetch_links"] = args.fetch_links
    if args.link_domains is not None:
        cfg["scan"]["link_domains"] = args.link_domains
    if args.link_timeout is not None:
        cfg["scan"]["link_timeout"] = args.link_timeout

    # 3) 凭证：user / auth（可从已有 secrets 取默认值；绝不写入 config）
    ex_user, ex_code = _read_existing_cred(acc["secrets_file"])
    user = args.user or _prompt("登录邮箱地址(user)", default=ex_user)
    # 未显式给 provider 时，由邮箱域名推导主机
    if not acc.get("provider") and not (args.imap_host or args.smtp_host) and user and "@" in user:
        dom = user.split("@")[-1].lower()
        prov = _DOMAIN_TO_PROVIDER.get(dom)
        if prov:
            acc["provider"] = prov
            print("[setup] 由邮箱域名推导 provider=%s" % prov)
    resolve_provider(acc)
    if args.auth_code:
        code = args.auth_code
    else:
        code = _prompt("IMAP/SMTP 授权码(auth code，不回显)", default=ex_code, secret=True)

    # 4) 校验关键项
    if not user:
        sys.exit("[setup] 错误：缺少登录邮箱地址（--user 或交互提供）")
    if not _is_email(user):
        sys.exit("[setup] 错误：邮箱地址格式无效：%r" % user)
    if not code:
        sys.exit("[setup] 错误：缺少授权码（--auth-code 或交互提供）")
    if not (acc.get("provider") or (acc.get("imap_host") and acc.get("smtp_host"))):
        sys.exit("[setup] 错误：未指定 provider 也未给 imap_host/smtp_host，无法确定邮件服务器")

    # 5) 连通性验证：授权码真的能用才写 secrets（保证写入准确）
    if not args.no_verify:
        print("[setup] 验证邮箱连通性（IMAP + SMTP）…")
        try:
            n = _imap_probe(cfg, user, code)
            print("  ✓ IMAP 登录成功，%s 共 %d 封" % (cfg["scan"]["folder"], n))
        except Exception as e:
            print("  ✗ IMAP 验证失败：%s" % e)
            _write_config_only(cfg, cfg_path)
            sys.exit("[setup] 授权码未通过验证，secrets 未写入；config.json 已保存，请修正后重跑 setup")
        try:
            _smtp_probe(cfg, user, code)
            print("  ✓ SMTP 登录成功")
        except Exception as e:
            print("  ✗ SMTP 验证失败：%s" % e)
            _write_config_only(cfg, cfg_path)
            sys.exit("[setup] 授权码未通过验证，secrets 未写入；config.json 已保存，请修正后重跑 setup")

    # 6) 写盘：config.json（无凭证） + secrets（600）
    _write_config_only(cfg, cfg_path)
    _write_secrets(acc["secrets_file"], user, code)
    print("\n[setup] 完成 ✅")
    print("  config ：%s" % cfg_path)
    print("  secrets：%s （权限 600）" % os.path.expanduser(acc["secrets_file"]))
    print("  转发收件人：%s" % (", ".join(cfg["forward"]["to"]) or "（未配置，scan 可跑，run 前需填）"))
    print("  抄送(CC)：%s" % (", ".join(cfg["forward"].get("cc") or []) or "（未启用，默认关闭）"))
    print("  下一步：%s check" % os.path.basename(__file__))


def main():
    ap = argparse.ArgumentParser(description="邮箱发票自动转发 v%s" % __version__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--config", default=os.environ.get("INVOICE_FORWARD_CONFIG", DEFAULT_CONFIG_PATH))

    sp = sub.add_parser("setup", parents=[parent], help="一次性配置：写 config.json + secrets(600)，并验证连通性")
    sp.add_argument("--user")
    sp.add_argument("--provider", help="qq/163/126/yeah 或域名；省略时由 --user 域名推导")
    sp.add_argument("--auth-code", help="IMAP/SMTP 授权码（省略则交互隐藏输入）")
    sp.add_argument("--imap-host")
    sp.add_argument("--smtp-host")
    sp.add_argument("--imap-port", type=int)
    sp.add_argument("--smtp-port", type=int)
    sp.add_argument("--to", nargs="+", help="转发收件人（多个空格分隔）")
    sp.add_argument("--folder", help="扫描文件夹，默认 INBOX")
    sp.add_argument("--days", type=int, help="扫描天数窗口")
    sp.add_argument("--subject-keywords", nargs="+", help="主题关键词（默认 发票）")
    sp.add_argument("--buyer-whitelist", nargs="*", help="抬头白名单（空=全部）")
    sp.add_argument("--subject-tpl", help="转发主题模板")
    sp.add_argument("--body-tpl", help="转发正文模板")
    sp.add_argument("--interval", type=int, help="发送节奏：每封最小间隔秒")
    sp.add_argument("--jitter", type=int, help="发送节奏：额外随机秒上限")
    sp.add_argument("--batch-limit", type=int, help="发送节奏：单批上限(0=不限)")
    sp.add_argument("--fetch-links", dest="fetch_links", action="store_true", default=None,
                    help="启用链接型发票抓取（扫描正文链接下载 PDF，默认开）")
    sp.add_argument("--no-fetch-links", dest="fetch_links", action="store_false",
                    help="禁用链接型发票抓取（仅处理 PDF 附件）")
    sp.add_argument("--link-domains", nargs="*",
                    help="仅下载这些域名后缀的链接（空=全部），如 myqcloud.com tencent.com")
    sp.add_argument("--link-timeout", type=int, help="链接下载超时秒")
    sp.add_argument("--no-verify", action="store_true", help="跳过 IMAP/SMTP 连通性验证")

    sp = sub.add_parser("check", parents=[parent])
    sp.add_argument("--install-deps", action="store_true",
                    help="缺少 PDF 解析库时自动 pip 安装到当前 Python 环境")
    for name in ("scan", "run"):
        sp = sub.add_parser(name, parents=[parent])
        sp.add_argument("--days", type=int, default=None)
    sp = sub.add_parser("parse", parents=[parent])
    sp.add_argument("pdf")
    args = ap.parse_args()

    if args.cmd == "setup":
        cmd_setup(args)
        return
    cfg, _ = load_config(args.config)
    if args.cmd == "check":
        cmd_check(cfg, install_deps=args.install_deps)
    elif args.cmd == "parse":
        try:
            with open(args.pdf, "rb") as fp:
                data = fp.read()
        except OSError as e:
            sys.exit("无法读取发票文件 %s：%s" % (args.pdf, e))
        fmt = detect_fmt_from_name(args.pdf) or detect_fmt_from_magic(data) or "pdf"
        if fmt == "pdf":
            try:
                import pdfplumber  # noqa
            except ImportError:
                try:
                    import fitz  # noqa
                except ImportError:
                    sys.exit("解析 PDF 需要 pdfplumber/pymupdf，请先执行：python3 %s check --install-deps"
                             % os.path.basename(__file__))
        f, _ = extract_invoice(data, fmt)
        print("[格式] %s" % fmt)
        print(json.dumps(f, ensure_ascii=False, indent=2))
    else:
        days = args.days or cfg["scan"]["days"]
        if not cfg["forward"]["to"]:
            sys.exit("config.json 的 forward.to 未配置收件人")
        process(cfg, days, do_send=(args.cmd == "run"))


if __name__ == "__main__":
    main()
