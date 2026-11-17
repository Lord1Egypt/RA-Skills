"""打包 life-coupon-expert 专家包 v1.1.0（推手模式：凭据内置，用户零配置）。

自检门禁（全过才出包）：
  R1 版本一致：plugin.json / README 均为 1.1.0；name/plugin/agentName 三者一致；
     agents 指向 agents/<agentName>.md 且文件真实存在
  R2 平台展示字段：displayDescription.zh 汉字数 >= 45 且总长 60-110；
     description <= 195 字符；tags 恰 3；quickPrompts 恰 3 且第一条 == defaultInitPrompt
  R3 skills 列表与 skills/ 目录一一对应（1 个：life-deal-finder）
  R4 无内部痕迹：liujycode / ljyit / 本机绝对路径 / __pycache__ / WorkBuddy-Output / 技能工厂
  R5 agent md frontmatter 必填字段齐，且覆盖 life-deal-finder 关键能力
  R6 SKILL.md version == 1.1.0；十个接口路径在 SKILL.md 中真实在列（能力不缩水）；
     凭据必须内置真实值（含「内置凭据」章节，无 YOUR_APIKEY 占位符，凭据值与本地 credentials 文件一致）
  R8 zip 结构：顶层 life-coupon-expert/ 目录 + 无 __MACOSX/.DS_Store + 头像 512x512 + LICENSE 在包
"""
import json
import os
import re
import struct
import sys
import zipfile

LS_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
PACKAGES_DIR = os.path.join(LS_ROOT, "packages")


def _batch_name(default_name):
    try:
        with open(os.path.join(PACKAGES_DIR, ".current_batch"), encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#"):
                    return line
    except Exception:
        pass
    import datetime
    return "%s-%s" % (default_name, datetime.date.today().strftime("%Y%m%d"))


SRC = os.path.dirname(os.path.abspath(__file__))
VERSION = "1.1.1"
ZIP_NAME = "life-coupon-expert"
OUT = os.path.join(PACKAGES_DIR, _batch_name("life-coupon"), "experts", f"{ZIP_NAME}-{VERSION}.zip")

os.chdir(SRC)
errors = []

# ---- R1 版本与名称一致 ----
pj = json.load(open(os.path.join(".codebuddy-plugin", "plugin.json"), encoding="utf-8"))
if pj["version"] != VERSION:
    errors.append(f"R1 plugin.json version={pj['version']} != {VERSION}")
readme = open("README.md", encoding="utf-8").read()
if VERSION not in readme:
    errors.append("R1 README 缺版本号")
if not (pj.get("name") == pj.get("plugin") == pj.get("agentName")):
    errors.append(f"R1 name/plugin/agentName 不一致：{pj.get('name')} / {pj.get('plugin')} / {pj.get('agentName')}")
expected_agent = f"./agents/{pj.get('agentName')}.md"
if pj.get("agents") != [expected_agent]:
    errors.append(f"R1 agents 应为 ['{expected_agent}']，实际 {pj.get('agents')}")
if not os.path.isfile(os.path.join("agents", f"{pj.get('agentName')}.md")):
    errors.append(f"R1 缺 agents/{pj.get('agentName')}.md")

# ---- R2 平台展示字段 ----
dd = pj["displayDescription"]["zh"]
_han = len(re.findall(r"[\u4e00-\u9fff]", dd))
if _han < 45:
    errors.append(f"R2 displayDescription 汉字数 {_han} < 45")
if not (60 <= len(dd) <= 110):
    errors.append(f"R2 displayDescription zh {len(dd)} 字，须 60-110")
_desc = pj.get("description", "")
if len(_desc) > 195:
    errors.append(f"R2 description {len(_desc)} 字符 > 195")
_dd_en = pj.get("displayDescription", {}).get("en", "")
if len(_dd_en) > 280:
    errors.append(f"R2 displayDescription.en {len(_dd_en)} > 280")
tags = pj["tags"]
qp = pj["quickPrompts"]
if len(tags) != 3:
    errors.append(f"R2 tags {len(tags)} != 3")
if len(qp) != 3:
    errors.append(f"R2 quickPrompts {len(qp)} != 3")
if qp[0]["zh"] != pj["defaultInitPrompt"]["zh"]:
    errors.append("R2 quickPrompts[0] != defaultInitPrompt")
for _i, _q in enumerate(qp):
    if len(_q.get("en", "")) > 58:
        errors.append(f"R2 quickPrompts[{_i}].en 超 58 字符")
_cm = re.search(r"分类：.+?（([\w-]+)）", readme)
if not _cm:
    errors.append("R2 README 未声明分类（应含『分类：xxx（categoryId）』）")
elif _cm.group(1) != pj.get("categoryId"):
    errors.append(f"R2 README 分类 {_cm.group(1)} != categoryId {pj.get('categoryId')}")
if pj.get("categoryId") not in {
    "01-ProductDesign", "02-Engineering", "03-GameSpatial", "04-DataAI",
    "05-MarketingGrowth", "06-ContentCreative", "07-SalesCommerce",
    "08-FinanceInvestment", "09-OperationsHR", "10-ProjectQuality",
    "11-SecurityCompliance", "12-IndustryConsultant",
}:
    errors.append(f"R2 categoryId {pj.get('categoryId')} 不在平台白名单 12 类内")

# ---- R3 skills 对应 ----
declared = {s.split("/")[-1] for s in pj["skills"]}
actual = {d for d in os.listdir("skills") if os.path.isdir(os.path.join("skills", d))}
if declared != actual:
    errors.append(f"R3 skills 不一致：declared={declared} actual={actual}")

# ---- R4 内部痕迹 ----
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in {"__pycache__", ".git", ".codebuddy-plugin"}]
    for f in files:
        p = os.path.join(root, f)
        if p.endswith("_pack.py"):
            continue
        if not p.lower().endswith((".md", ".json", ".py", ".txt")):
            continue
        data = open(p, "rb").read()
        for marker in (b"liujycode", b"ljyit", b"D:\\work", b"D:/work", b"C:\\Users",
                       "技能工厂".encode("utf-8"), "WorkBuddy-Output".encode("utf-8"),
                       "并行批次".encode("utf-8")):
            if marker in data:
                errors.append(f"R4 {p} 含内部痕迹 {marker}")

# ---- R5 agent md ----
agent = open(os.path.join("agents", f"{pj['agentName']}.md"), encoding="utf-8").read()
_am = re.search(r'^description:\s*"?([^"\n]+)"?\s*$', agent, re.M)
if _am and len(_am.group(1)) > 195:
    errors.append(f"R5 agent md description {len(_am.group(1))} 字符 > 195")
for field in ("name:", "description:", "displayName:", "profession:", "maxTurns:"):
    if field not in agent:
        errors.append(f"R5 agent md 缺 {field}")
for kw in ("life-deal-finder", "现查现给", "凭据已内置", "合规"):
    if kw not in agent:
        errors.append(f"R5 agent md 未覆盖关键能力（{kw}）")

# ---- R6 SKILL.md 版本与发布接口（订单对账禁入）----
skill = open(os.path.join("skills", "life-deal-finder", "SKILL.md"), encoding="utf-8-sig").read()
m = re.search(r"^version:[ \t]*(\S+)", skill, re.M)
if not m or m.group(1) != VERSION:
    errors.append(f"R6 SKILL.md version={m and m.group(1)} != {VERSION}")
endpoints = [
    "meituan_activity_list", "meituan_ratesurl", "elm_activity_list",
    "elm_activity_ratesurl", "hv_ratesurl", "tchotel_ratesurl",
    "supersearch", "ratesurl",
]
for ep in endpoints:
    if ep not in skill:
        errors.append(f"R6 SKILL.md 缺接口 {ep}")
# 2026-10-31 收口：订单/佣金对账接口为开发者侧，发布包不得再包含其路径与样例
# （包内 key 泄露最多被拿去转链=替我们推广，但流水是隐私，文档样例也不该教人打）
for ep in ("mt_order_list", "elm_order_list"):
    if ep in skill:
        errors.append(f"R6 SKILL.md 泄露订单对账接口 {ep}（开发者侧，不入包）")
for section in ("内置凭据", "接口速查", "工作流程", "输出规范", "合规红线", "常见问题"):
    if section not in skill:
        errors.append(f"R6 SKILL.md 缺章节 {section}")
# 推手模式：凭据必须内置真实值，不得退化为占位符
if "YOUR_APIKEY" in skill:
    errors.append("R6 SKILL.md 仍含 YOUR_APIKEY 占位符（推手模式要求凭据内置）")
_cred_path = os.path.join(LS_ROOT, "src", "projects", "life-coupon-agent", "credentials", "config_local.md")
if os.path.isfile(_cred_path):
    _cred = open(_cred_path, encoding="utf-8").read()
    _mk = re.search(r"APIKEY[:：]\s*(\w+)", _cred)
    _mp = re.search(r"PID[:：]\s*(mm_\w+)", _cred)
    _mt = re.search(r"tb_name\(授权淘宝账号昵称\)[:：]\s*([^\s（]+)", _cred)
    if _mk and _mk.group(1) not in skill:
        errors.append("R6 SKILL.md 内置 ApiKey 与 credentials 文件不一致")
    if _mp and _mp.group(1) not in skill:
        errors.append("R6 SKILL.md 内置 PID 与 credentials 文件不一致")
    if _mt and _mt.group(1) not in skill:
        errors.append("R6 SKILL.md 内置 tb_name 与 credentials 文件不一致")
else:
    errors.append("R6 找不到 credentials/config_local.md，无法校验内置凭据")
# YAML 半角冒号坑：frontmatter 值里不允许 "半角冒号+空格"
fm = skill.split("---")[1]
for line in fm.splitlines():
    if re.match(r"^[a-zA-Z_]+: .*(?<!http)(?<!https):\s", line):
        errors.append(f"R6 frontmatter 疑似半角冒号坑：{line.strip()[:60]}")

# ---- R11 许可证 ----
if not os.path.isfile("LICENSE"):
    errors.append("R11 包根缺 LICENSE")
if not pj.get("license"):
    errors.append("R11 plugin.json 缺 license 字段")

# ---- R12 agents md 引用的包内文件必须真实存在 ----
_REF_TOK = re.compile(r"(?:skills|scripts|assets|references|templates|examples|tools|agents|avatars)"
                      r"/[^\s`'\")\u3002\uff0c\uff1b\u3001]+")
for md in sorted(d for d in os.listdir("agents") if d.endswith(".md")):
    txt = open(os.path.join("agents", md), encoding="utf-8").read()
    for mref in _REF_TOK.finditer(txt):
        p = mref.group(0).rstrip(".,;")
        if any(c in p for c in "<>{}*$"):
            errors.append(f"R12 agents/{md} 引用含占位符：{p}")
        elif not os.path.exists(p.replace("/", os.sep)):
            errors.append(f"R12 agents/{md} 引用了包内不存在的文件：{p}")

if errors:
    print("门禁未过：")
    for e in errors:
        print("  " + e)
    sys.exit(1)


def add_dir(zf, dirname):
    for root, dirs, files in os.walk(dirname):
        dirs[:] = [d for d in dirs if d not in {"__pycache__", ".git"}]
        for f in sorted(files):
            full = os.path.join(root, f)
            rel = os.path.relpath(full, ".")
            zf.write(full, f"{ZIP_NAME}/{rel}")


os.makedirs(os.path.dirname(OUT), exist_ok=True)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
    for item in (".codebuddy-plugin", "agents", "avatars", "skills", "README.md", "LICENSE"):
        if os.path.isdir(item):
            add_dir(zf, item)
        else:
            zf.write(item, f"{ZIP_NAME}/{item}")

# ---- R8 zip 结构复扫 ----
with zipfile.ZipFile(OUT) as zf:
    names = zf.namelist()
    if any(n.startswith("__MACOSX") or n.endswith(".DS_Store") for n in names):
        errors.append("R8 zip 含垃圾文件")
    if f"{ZIP_NAME}/.codebuddy-plugin/plugin.json" not in names:
        errors.append("R8 zip 缺顶层 plugin.json")
    if f"{ZIP_NAME}/LICENSE" not in names:
        errors.append("R8 zip 缺 LICENSE")
    if f"{ZIP_NAME}/avatars/expert.png" not in names:
        errors.append("R8 zip 缺头像")
    else:
        with zf.open(f"{ZIP_NAME}/avatars/expert.png") as f:
            head = f.read(33)
        if head[:8] != b"\x89PNG\r\n\x1a\n":
            errors.append("R8 头像不是 PNG")
        else:
            w, h = struct.unpack(">II", head[16:24])
            if (w, h) != (512, 512):
                errors.append(f"R8 头像尺寸 {(w, h)} != (512, 512)")
    if zf.testzip():
        errors.append("R8 zip 损坏")

if errors:
    print("R8 失败：")
    for e in errors:
        print("  " + e)
    sys.exit(1)

size = os.path.getsize(OUT) / 1024
print(f"OK：{OUT}（{len(names)} 项，{size:.1f} KB）")
