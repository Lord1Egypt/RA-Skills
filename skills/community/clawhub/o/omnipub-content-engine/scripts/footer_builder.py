# -*- coding: utf-8 -*-
"""
Footer Builder Module
======================
Assembles article footer HTML from config (QR codes, intro, past articles, CTA).

Usage:
    python footer_builder.py --config config.yaml --output footer.html
    python footer_builder.py --config config.yaml --format markdown
"""
import argparse
import json
import os
import sys

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def build_footer_html(config: dict) -> str:
    brand = config.get("brand", {})
    footer_cfg = config.get("footer", {})
    order = footer_cfg.get("order", ["recommend", "about", "community", "cta", "signature"])

    sections = []
    for section in order:
        if section == "recommend":
            articles = brand.get("past_articles", [])
            if articles:
                items = "".join(
                    f'<p style="margin:0 0 8px;font-size:14px;color:#534AB7;">'
                    f'<a href="{a["url"]}" style="color:#534AB7;text-decoration:none;">'
                    f'{a["title"]}</a></p>'
                    for a in articles
                )
                sections.append(
                    f'<section style="margin:24px 0;padding:16px;border-top:1px solid #eee;">'
                    f'<p style="font-size:13px;font-weight:500;color:#639922;margin:0 0 12px;">'
                    f'推荐阅读</p>{items}</section>'
                )

        elif section == "about":
            bio = brand.get("bio", "")
            name = brand.get("name", "")
            if bio:
                sections.append(
                    f'<section style="margin:24px 0;padding:16px;border-top:1px solid #eee;">'
                    f'<p style="font-size:13px;font-weight:500;color:#639922;margin:0 0 8px;">'
                    f'关于{name}</p>'
                    f'<p style="font-size:14px;line-height:1.75;color:#333;margin:0;">{bio}</p>'
                    f'</section>'
                )

        elif section == "community":
            wechat_qr = brand.get("wechat_qr", "")
            community_qr = brand.get("community_qr", "")
            qr_html = ""
            if wechat_qr:
                qr_html += f'<img src="{wechat_qr}" style="width:120px;height:120px;margin:0 8px;" alt="微信二维码"/>'
            if community_qr:
                qr_html += f'<img src="{community_qr}" style="width:120px;height:120px;margin:0 8px;" alt="社群二维码"/>'
            if qr_html:
                sections.append(
                    f'<section style="margin:24px 0;padding:16px;border-top:1px solid #eee;text-align:center;">'
                    f'<p style="font-size:13px;font-weight:500;color:#639922;margin:0 0 12px;">'
                    f'扫码连接</p>{qr_html}</section>'
                )

        elif section == "cta":
            sections.append(
                f'<section style="margin:24px 0;padding:16px;border-top:1px solid #eee;text-align:center;">'
                f'<p style="font-size:15px;color:#534AB7;font-weight:500;margin:0;">'
                f'关注{brand.get("name","")}，获取更多增长干货</p>'
                f'</section>'
            )

        elif section == "signature":
            sections.append(
                f'<section style="margin:16px 0;text-align:center;">'
                f'<p style="font-size:12px;color:#999;margin:0;">— END —</p>'
                f'</section>'
            )

    return "\n".join(sections)


def build_footer_markdown(config: dict) -> str:
    brand = config.get("brand", {})
    footer_cfg = config.get("footer", {})
    order = footer_cfg.get("order", ["recommend", "about", "community", "cta", "signature"])

    lines = []
    for section in order:
        if section == "recommend":
            articles = brand.get("past_articles", [])
            if articles:
                lines.append("---\n**推荐阅读**")
                for a in articles:
                    lines.append(f"- [{a['title']}]({a['url']})")
                lines.append("")

        elif section == "about":
            bio = brand.get("bio", "")
            name = brand.get("name", "")
            if bio:
                lines.append(f"**关于{name}**\n\n{bio}\n")

        elif section == "community":
            wechat_qr = brand.get("wechat_qr", "")
            community_qr = brand.get("community_qr", "")
            if wechat_qr:
                lines.append(f"![微信二维码]({wechat_qr})")
            if community_qr:
                lines.append(f"![社群二维码]({community_qr})")
            lines.append("")

        elif section == "cta":
            lines.append(f"**关注{brand.get('name','')}，获取更多增长干货**\n")

        elif section == "signature":
            lines.append("---\n— END —\n")

    return "\n".join(lines)


def load_config(config_path: str) -> dict:
    with open(config_path, encoding="utf-8") as f:
        if config_path.endswith(".json"):
            return json.load(f)
        return yaml.safe_load(f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build article footer from config")
    parser.add_argument("--config", required=True, help="Config file path (YAML or JSON)")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--format", choices=["html", "markdown"], default="html", help="Output format")
    args = parser.parse_args()

    config = load_config(args.config)
    if args.format == "html":
        output = build_footer_html(config)
    else:
        output = build_footer_markdown(config)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Footer saved: {args.output}")
    else:
        print(output)
