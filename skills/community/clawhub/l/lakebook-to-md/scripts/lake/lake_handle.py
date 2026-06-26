from bs4 import BeautifulSoup, NavigableString, Tag
import json
import urllib
import queue
import os
import requests
import time
import re


def remove_invalid_characters(filename):
    """移除文件路径中的非法字符"""
    p = r"^[a-zA-Z]:"
    prefix = ""
    h = re.match(p, filename)
    if h:
        regs = h.regs
        prefix = filename[regs[0][0] : regs[0][1]]
        filename = filename.replace(prefix, "")
    invalid_chars = r'[<>:"|?*]'
    cleaned_filename = re.sub(invalid_chars, "", filename)
    return prefix + cleaned_filename


class MyContext:
    def __init__(
        self, filename="xxx", download_image=True, image_target="", skip_existing=False
    ):
        self.template_queue = queue.Queue()
        self.result = ""
        self.filename = filename + ".assert"
        self.image_target = image_target
        self.failure_images = []
        self.download_image = download_image
        self.skip_existing = skip_existing
        self.downloaded_files = []  # 成功下载的文件
        self.failed_files = []  # 下载失败的文件
        self.expired_links = []  # 过期的链接

    def append_failure(self, name, image_src):
        r = "[{}]{}".format(name, image_src)
        self.failure_images.append(r)

    def add_downloaded_file(self, name, url, local_path):
        self.downloaded_files.append({"name": name, "url": url, "path": local_path})

    def add_failed_file(self, name, url, error):
        self.failed_files.append({"name": name, "url": url, "error": error})

    def add_expired_link(self, name, url):
        self.expired_links.append({"name": name, "url": url})

    def find_file_path(self, file_uid):
        return file_uid


def eventual_tag(tag: Tag) -> bool:
    return len(tag.contents) == 0 or (
        len(tag.contents) == 1 and isinstance(tag.contents[0], NavigableString)
    )


class MyParser:
    """语雀 lake ASL 格式解析器，将 HTML 标签转换为 Markdown"""

    def __init__(self, htmlText):
        self.soup = BeautifulSoup(htmlText, "html.parser")
        self.tagQueue = queue.Queue()

    def handle_descent(self, tag: Tag, context1: MyContext) -> str:
        tag_name = tag.name
        if tag_name == "span":
            return self.handle_span(tag, context1)
        elif tag_name == "p":
            return self.handle_p(tag, context1)
        elif tag_name in ("h1", "h2", "h3", "h4", "h5", "h6", "h7"):
            return self.handle_title(tag, int(tag_name[1]), context1)
        elif tag_name == "blockquote":
            return self.handle_blockquote(tag, context1)
        elif tag_name == "card":
            return self.handle_card(tag, context1)
        elif tag_name == "strong":
            return self.handle_strong(tag, context1)
        elif tag_name == "em":
            return self.handle_em(tag, context1)
        elif tag_name == "del":
            return self.handle_del(tag, context1)
        elif tag_name == "u":
            return self.handle_u(tag, context1)
        elif tag_name == "sup":
            return self.handle_sup(tag, context1)
        elif tag_name == "sub":
            return self.handle_sub(tag, context1)
        elif tag_name == "code":
            return self.handle_code(tag, context1)
        elif tag_name == "ul":
            return self.handle_ul(tag, context1)
        elif tag_name == "ol":
            return self.handle_ol(tag, context1)
        elif tag_name == "a":
            return self.handle_a(tag, context1)
        elif tag_name == "table":
            return self.handle_table(tag, context1)
        elif tag_name == "li":
            return self.handle_li(tag, context1)
        elif tag_name == "br":
            return "\n"
        else:
            return self.handle_common(context1, tag)

    # ==================== 标题 ====================

    def handle_title(self, tag, level, context1):
        prefix = "#" * level + " {}\n"
        if eventual_tag(tag):
            return prefix.format(tag.text if len(tag) > 0 else "")
        return prefix.format(self.handle_common(context1, tag))

    def handle_blockquote(self, tag, context1):
        template = "> {}\n"
        if eventual_tag(tag):
            return template.format(tag.text if len(tag) > 0 else "")
        return template.format(self.handle_common(context1, tag))

    def handle_li(self, tag, context1):
        if eventual_tag(tag):
            return tag.text if len(tag) > 0 else ""
        return self.handle_common(context1, tag)

    # ==================== 卡片处理 ====================

    def handle_card(self, tag, context1):
        name = tag.attrs.get("name")
        value = tag.attrs.get("value")
        if not value:
            return "\n"
        value = value[5:]
        data = urllib.parse.unquote(value, encoding="utf-8")
        data_json = json.loads(data)

        if name == "codeblock":
            # 代码块
            mode = data_json.get("mode", "plain")
            code = data_json.get("code", "")
            card_name = data_json.get("name", "")
            return "{0}\n```{1}\n{2}\n```\n".format(card_name, mode, code)
        elif name == "image":
            # 图片
            card_name = data_json.get("name", "")
            card_name, rel_path = self.download_resource(context1, data_json, card_name)
            return "![{}]({})\n".format(card_name, "./" + rel_path)
        elif name == "hr":
            # 分割线
            return "\n---\n"
        elif name == "label":
            # 标签
            return data_json.get("label", "")
        elif name == "math":
            # 数学公式
            la_tex = data_json.get("code", "")
            card_name, rel_path = self.download_resource(
                context1, data_json, "数学公式"
            )
            return la_tex + "\n" + "![{}]({})\n".format(card_name, "./" + rel_path)
        elif name == "file":
            # 文件附件
            card_name = data_json.get("name", "")
            card_name, rel_path = self.download_resource(context1, data_json, card_name)
            return "![{}]({})\n".format(card_name, "./" + rel_path)
        elif name == "yuque":
            # 跨文档引用
            src = data_json.get("src", "")
            file_uid = src.split("/")[-1] if src else ""
            title = data_json.get("detail", {}).get("title", "")
            path = context1.find_file_path(file_uid)
            return "[{}]({})".format(title, path)
        elif name == "lockedtext":
            # 加密锁定内容（AES-256-GCM，密钥不在导出中，无法解密）
            return "\n> [加密内容 - 该部分内容在语雀中已加密锁定，无法导出]\n"
        elif name == "bookmarkInline":
            # 链接书签（带标题、来源、描述）
            src = data_json.get("src", "")
            text = data_json.get("text", src)
            detail = data_json.get("detail", {})
            title = detail.get("title", text)
            belong = detail.get("belong", "")
            desc = detail.get("desc", "")
            lines = []
            if belong:
                lines.append(f"\n> **[{title}]({src})** — {belong}")
            else:
                lines.append(f"\n> **[{title}]({src})**")
            if desc:
                desc_short = desc[:200] + "..." if len(desc) > 200 else desc
                lines.append(f"> {desc_short}")
            lines.append("")
            return "\n".join(lines)
        elif name == "bookmarklink":
            # 链接书签（简单链接）
            src = data_json.get("src", "")
            text = data_json.get("text", src)
            detail = data_json.get("detail", {})
            title = detail.get("title", text)
            return f"[{title}]({src})\n"
        elif name == "localdoc":
            # 本地附件（PDF 等，OSS 签名链接可能过期）
            src = data_json.get("src", "")
            download_src = data_json.get("downloadSrc", src)
            file_name = data_json.get("name", "附件")
            size = data_json.get("size", 0)
            ext = data_json.get("ext", "")

            if size > 1024 * 1024:
                size_str = f"{size / 1024 / 1024:.1f} MB"
            elif size > 1024:
                size_str = f"{size / 1024:.0f} KB"
            else:
                size_str = f"{size} B"

            # 尝试下载附件
            if download_src and context1.download_image:
                try:
                    # 构建本地路径
                    local_dir = os.path.join(context1.image_target, context1.filename)
                    if not os.path.exists(local_dir):
                        os.makedirs(local_dir, exist_ok=True)

                    # 清理文件名
                    safe_name = re.sub(r'[<>:"|?*]', "_", file_name)
                    local_path = os.path.join(local_dir, safe_name)

                    # 检查是否已存在
                    if context1.skip_existing and os.path.exists(local_path):
                        rel_path = os.path.relpath(local_path, context1.image_target)
                        context1.add_downloaded_file(file_name, download_src, rel_path)
                        return f"\n[{file_name}]({rel_path}) ({size_str})\n"

                    # 下载文件
                    time.sleep(0.5)
                    resp = requests.get(download_src, timeout=30)
                    if resp.status_code == 200:
                        with open(local_path, "wb") as f:
                            f.write(resp.content)
                        rel_path = os.path.relpath(local_path, context1.image_target)
                        context1.add_downloaded_file(file_name, download_src, rel_path)
                        return f"\n[{file_name}]({rel_path}) ({size_str})\n"
                    else:
                        context1.add_failed_file(
                            file_name, download_src, f"HTTP {resp.status_code}"
                        )
                        context1.append_failure(file_name, download_src)
                        return f"\n[{file_name}]({download_src}) ({size_str}) [下载失败: HTTP {resp.status_code}]\n"

                except Exception as e:
                    context1.add_failed_file(file_name, download_src, str(e))
                    context1.append_failure(file_name, download_src)
                    return f"\n[{file_name}]({download_src}) ({size_str}) [下载失败: {str(e)}]\n"

            elif download_src:
                # 有链接但未下载（禁用下载模式）
                return f"\n[{file_name}]({download_src}) ({size_str})\n"
            else:
                # 链接已过期
                context1.add_expired_link(file_name, src)
                return f"\n{file_name} ({size_str}) [下载链接已过期]\n"
        else:
            return "\n"

    def download_resource(self, context1, data_json, name):
        """下载图片或附件资源"""
        src = data_json["src"]
        resource_name = src.split("/")[-1]
        full_image_name = "/".join(
            [context1.image_target, context1.filename, resource_name]
        )
        full_image_path = "/".join([context1.image_target, context1.filename])
        relative_image_path = "/".join([context1.filename, resource_name])
        if not name:
            name = full_image_name
        if context1.filename != "":
            if not os.path.exists(full_image_path):
                full_image_path = remove_invalid_characters(full_image_path)
                os.makedirs(full_image_path, exist_ok=True)
            try:
                if context1.download_image:
                    full_image_name = remove_invalid_characters(full_image_name)
                    if context1.skip_existing and os.path.exists(full_image_name):
                        return name, relative_image_path
                    time.sleep(0.5)
                    resp = requests.get(src)
                    if resp.status_code != 200:
                        raise Exception(
                            "下载失败：{}, 状态码: {}".format(src, resp.status_code)
                        )
                    with open(full_image_name, "wb") as imageFp:
                        imageFp.write(resp.content)
                        imageFp.flush()
            except Exception as ex:
                context1.append_failure(name, src)
                print("附件 {} 下载失败".format(src))
                name = "附件下载失败"
        return name, relative_image_path

    # ==================== 文本格式 ====================

    def handle_span(self, tag, context1):
        if eventual_tag(tag):
            return tag.text if len(tag) > 0 else ""
        return self.handle_common(context1, tag)

    def handle_p(self, tag, context1):
        if eventual_tag(tag):
            return (tag.text + "\n") if len(tag) > 0 else "\n"
        return self.handle_common(context1, tag) + "\n"

    def handle_common(self, context1, tag):
        temp_str = ""
        for _tag in tag.contents:
            if isinstance(_tag, NavigableString):
                if tag.name == "[document]":
                    continue
                temp_str += _tag
                continue
            temp_str += self.handle_descent(_tag, context1)
        return temp_str

    def handle_strong(self, tag, context1):
        t = "**{}**"
        if eventual_tag(tag):
            return t.format(tag.text if len(tag) > 0 else "")
        return t.format(self.handle_common(context1, tag))

    def handle_em(self, tag, context1):
        t = "*{}*"
        if eventual_tag(tag):
            return t.format(tag.text if len(tag) > 0 else "")
        return t.format(self.handle_common(context1, tag))

    def handle_del(self, tag, context1):
        t = "~~{}~~"
        if eventual_tag(tag):
            return t.format(tag.text if len(tag) > 0 else "")
        return t.format(self.handle_common(context1, tag))

    def handle_u(self, tag, context1):
        t = "<u>{}</u>"
        if eventual_tag(tag):
            return t.format(tag.text if len(tag) > 0 else "")
        return t.format(self.handle_common(context1, tag))

    def handle_sup(self, tag, context1):
        t = "^{}"
        if eventual_tag(tag):
            return t.format(tag.text if len(tag) > 0 else "")
        return t.format(self.handle_common(context1, tag))

    def handle_sub(self, tag, context1):
        t = "~{}"
        if eventual_tag(tag):
            return t.format(tag.text if len(tag) > 0 else "")
        return t.format(self.handle_common(context1, tag))

    def handle_code(self, tag, context1):
        t = "`{}`"
        if eventual_tag(tag):
            return t.format(tag.text if len(tag) > 0 else "")
        return t.format(self.handle_common(context1, tag))

    # ==================== 列表 ====================

    def handle_ul(self, tag, context1):
        if eventual_tag(tag):
            return "- {}\n".format(tag.text if len(tag) > 0 else "")
        tempStr = ""
        for _tag in tag.contents:
            if isinstance(_tag, NavigableString):
                tempStr += _tag
                continue
            if _tag.name == "li":
                r = self.handle_common(context1, _tag)
                tempStr += "\n- " + r
            else:
                tempStr += self.handle_common(context1, _tag)
        return tempStr

    def handle_ol(self, tag, context1):
        if eventual_tag(tag):
            return "1. {}".format(tag.text if len(tag) > 0 else "")
        tempStr = ""
        count = 1
        for _tag in tag.contents:
            if isinstance(_tag, NavigableString):
                tempStr += _tag
                continue
            if _tag.name == "li":
                r = self.handle_common(context1, _tag)
                tempStr += "\n{}. {}".format(count, r)
                count += 1
            else:
                tempStr += self.handle_common(context1, _tag)
        return tempStr

    # ==================== 链接 ====================

    def handle_a(self, tag, context1):
        href = tag.attrs.get("href", "")
        if eventual_tag(tag):
            return "[{}]({})".format(tag.text if len(tag) > 0 else "链接", href)
        r = self.handle_common(context1, tag)
        return "[{}]({})".format(r, href)

    # ==================== 表格 ====================

    def handle_table(self, tag, context1):
        tbody = tag.tbody
        if not tbody:
            return ""
        table_str = ""
        row_count = 0
        col_num = 0
        for _tr in tbody.contents:
            if isinstance(_tr, NavigableString):
                continue
            row = " | "
            for _td in _tr.contents:
                if isinstance(_td, NavigableString):
                    continue
                if row_count == 0:
                    col_num += 1
                r = self.handle_common(context1, _td)
                r = r.replace("\n", "")
                row += r + " | "
            row += "\n"
            table_str += row
            if row_count == 0:
                separate = "|" + "|".join(["---" for _ in range(0, col_num)]) + "|\n"
                table_str += separate
            row_count += 1
        return table_str
