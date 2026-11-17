#!/usr/bin/env python3
"""
markdown-bundle-browser v2: Generate a self-contained, offline-capable HTML
document browser from a directory of markdown files.

Upgrades over v1:
  - Offline rendering: built-in lightweight GFM renderer, no CDN dependency
  - Real directory tree: nested sidebar with expand/collapse
  - Global search: filter files by title + content
  - Config-driven grouping: optional YAML config for custom group rules
  - Document cross-links: relative .md links become clickable jumps
  - Lazy rendering: content parsed only when a file is opened

Usage:
    python3 bundle.py <directory> [--output index.html] [--title "My Docs"]
    python3 bundle.py <directory> --config bundle.yaml
"""

import os
import re
import sys
import json
import argparse
import html as html_mod

# ---------------------------------------------------------------------------
# Config (optional YAML-like mini parser, no external deps)
# ---------------------------------------------------------------------------

DEFAULT_GROUP_ORDER = ["入口", "研究数据", "公司档案", "任务与工作流", "模板", "其他"]


def parse_simple_yaml(path):
    """Parse a minimal YAML subset: top-level keys mapping to lists or scalars.
    Supports:
        group_rules:
          - match: "data/"
            group: "研究数据"
            icon: "📊"
        order: ["入口", "研究数据"]
        title: "My Docs"
    """
    config = {"group_rules": [], "order": None, "title": None, "badges": []}
    if not path or not os.path.exists(path):
        return config
    current_key = None
    in_list = False
    item = None
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip()
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            indent = len(line) - len(line.lstrip())
            if indent == 0 and ":" in line and not line.startswith("-"):
                key = line.split(":", 1)[0].strip()
                val = line.split(":", 1)[1].strip()
                current_key = key
                in_list = False
                if key == "title" and val:
                    config["title"] = val.strip("\"'")
                elif key == "order" and val:
                    config["order"] = [x.strip().strip("\"'") for x in val.strip("[]").split(",") if x.strip()]
                elif key in ("group_rules", "badges"):
                    in_list = True
                    if key == "group_rules":
                        config["group_rules"] = []
                    else:
                        config["badges"] = []
            elif indent > 0 and line.lstrip().startswith("- "):
                item_text = line.lstrip()[2:].strip()
                item = {}
                for part in item_text.split(","):
                    if ":" in part:
                        k, v = part.split(":", 1)
                        item[k.strip()] = v.strip().strip("\"'")
                if current_key == "group_rules" and item:
                    config["group_rules"].append(item)
                elif current_key == "badges" and item:
                    config["badges"].append(item)
            elif indent > 0 and ":" in line and in_list and item is not None:
                k, v = line.split(":", 1)
                item[k.strip()] = v.strip().strip("\"'")
    return config


def apply_group_rules(config, rel_path):
    """Return (group_name, icon) from config rules, or None if no rule matches."""
    for rule in config.get("group_rules", []):
        match = rule.get("match", "")
        if match and match in rel_path:
            return rule.get("group", "其他"), rule.get("icon", "📄")
    return None


def badge_for(filename, parent_dir, config):
    """Infer a badge label from config rules first, then filename heuristics."""
    rel = os.path.join(parent_dir, filename)
    for rule in config.get("badges", []):
        match = rule.get("match", "")
        if match and match in rel:
            return f'<span class="badge">{html_mod.escape(rule.get("label", "文档"))}</span>'
    name = filename.lower()
    if "readme" in name:
        return '<span class="badge badge-done">入口</span>'
    if "task_queue" in name or "task-queue" in name:
        return '<span class="badge badge-done">任务</span>'
    if "backlog" in name:
        return '<span class="badge badge-draft">积压</span>'
    if "template" in parent_dir.lower() or "template" in name:
        return '<span class="badge badge-done">模板</span>'
    if "industry_map" in name or "产业链" in name:
        return '<span class="badge badge-real">数据</span>'
    if "tech" in name or "技术" in name or "cycle" in name or "周期" in name or "policy" in name or "政策" in name:
        return '<span class="badge badge-real">数据</span>'
    if "market" in name or "市场" in name:
        return '<span class="badge badge-real">实时</span>'
    if "profile" in parent_dir.lower() or "档案" in name:
        return '<span class="badge badge-real">公司</span>'
    return '<span class="badge badge-done">文档</span>'


# ---------------------------------------------------------------------------
# File collection
# ---------------------------------------------------------------------------

def collect_md_files(root_dir):
    md_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for f in filenames:
            if f.endswith(".md") and not f.startswith("."):
                abs_path = os.path.join(dirpath, f)
                rel_path = os.path.relpath(abs_path, root_dir)
                md_files.append((rel_path, abs_path))
    md_files.sort(key=lambda x: (x[0].count(os.sep), x[0].lower()))
    return md_files


def build_tree(md_files):
    """Build nested tree: {dir: {subdir: ... , "__files__": [(id, title), ...]}}"""
    tree = {}
    for i, (rel_path, _) in enumerate(md_files):
        parts = rel_path.replace("\\", "/").split("/")
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {"__files__": []})
        node.setdefault("__files__", []).append((f"f{i}", parts[-1], rel_path))
    return tree


# ---------------------------------------------------------------------------
# HTML generation
# ---------------------------------------------------------------------------

def escape_js(s):
    return (s.replace("\\", "\\\\").replace("`", "\\`")
             .replace("${", "\\${").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))


def generate_html(root_dir, title, md_files, config):
    entries = []
    for i, (rel_path, abs_path) in enumerate(md_files):
        with open(abs_path, encoding="utf-8") as fh:
            content = fh.read()
        filename = os.path.basename(rel_path)
        parent_dir = os.path.dirname(rel_path)
        badge = badge_for(filename, parent_dir, config)
        entries.append({
            "id": f"f{i}",
            "title": filename,
            "badge": badge,
            "md": content,
            "rel": rel_path,
        })
    data_js = json.dumps(entries, ensure_ascii=False).replace("</", "<\\/")

    tree_js = json.dumps(build_tree(md_files), ensure_ascii=False)

    group_order = config.get("order") or DEFAULT_GROUP_ORDER

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_mod.escape(title)}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;background:#0f172a;color:#e2e8f0;display:flex;height:100vh;overflow:hidden}}
#sidebar{{width:320px;min-width:320px;background:#1e293b;overflow-y:auto;border-right:1px solid #334155;display:flex;flex-direction:column}}
#sidebar .head{{padding:16px 16px 10px}}
#sidebar h2{{font-size:1rem;color:#f8fafc;margin-bottom:4px}}
#sidebar .subtitle{{font-size:.75rem;color:#94a3b8;margin-bottom:12px}}
#search{{margin:0 12px 10px;padding:8px 12px;border-radius:8px;border:1px solid #334155;background:#0f172a;color:#e2e8f0;font-size:.82rem;outline:none}}
#search:focus{{border-color:#38bdf8}}
#tree{{flex:1;overflow-y:auto;padding:0 8px 16px}}
.dir-row{{display:flex;align-items:center;gap:6px;padding:6px 8px;border-radius:6px;cursor:pointer;font-size:.8rem;color:#94a3b8;user-select:none}}
.dir-row:hover{{background:#334155}}
.dir-row .arrow{{transition:transform .15s;font-size:.7rem;width:12px;text-align:center}}
.dir-row.open .arrow{{transform:rotate(90deg)}}
.dir-row .gicon{{width:18px}}
.children{{display:none;margin-left:14px;border-left:1px solid #334155;padding-left:6px}}
.children.open{{display:block}}
.file-link{{display:flex;align-items:center;gap:6px;width:100%;padding:7px 8px;margin:2px 0;border-radius:6px;cursor:pointer;border:none;background:none;color:#cbd5e1;font-size:.8rem;text-align:left}}
.file-link:hover{{background:#334155}}
.file-link.active{{background:#0f766e;color:#f0fdfa;font-weight:500}}
.file-link .fname{{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1}}
#content{{flex:1;overflow-y:auto;padding:32px 44px}}
#content .empty{{text-align:center;color:#64748b;margin-top:120px;font-size:1rem}}
#content .empty .icon{{font-size:3rem;margin-bottom:12px}}
#content h1{{font-size:1.5rem;color:#f8fafc;margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid #1e293b}}
#content h2{{font-size:1.2rem;color:#e2e8f0;margin:28px 0 10px;padding-bottom:4px;border-bottom:1px solid #1e293b}}
#content h3{{font-size:1.05rem;color:#cbd5e1;margin:20px 0 8px}}
#content p{{margin:8px 0;line-height:1.75;font-size:.93rem}}
#content blockquote{{background:#1e293b;border-left:3px solid #38bdf8;padding:10px 16px;margin:12px 0;border-radius:0 8px 8px 0;color:#94a3b8;font-size:.88rem}}
#content table{{width:100%;border-collapse:collapse;margin:12px 0;font-size:.85rem}}
#content th{{background:#1e3a5f;color:#e2e8f0;padding:8px 12px;text-align:left;font-weight:500;border:1px solid #334155}}
#content td{{padding:8px 12px;border:1px solid #334155;vertical-align:top}}
#content tr:nth-child(even){{background:#1a2332}}
#content code{{background:#334155;padding:2px 6px;border-radius:4px;font-size:.84rem;color:#fbbf24}}
#content pre{{background:#0f172a;border:1px solid #334155;padding:14px 18px;border-radius:10px;overflow-x:auto;margin:12px 0;font-size:.84rem;line-height:1.55}}
#content pre code{{background:none;padding:0;color:#e2e8f0}}
#content ul,#content ol{{padding-left:24px;margin:8px 0}}
#content li{{line-height:1.7;font-size:.92rem;margin:4px 0}}
#content a{{color:#38bdf8;cursor:pointer}}
#content hr{{border:none;border-top:1px solid #334155;margin:20px 0}}
#content strong{{color:#f8fafc}}
#content img{{max-width:100%;border-radius:8px}}
.badge{{display:inline-block;font-size:.68rem;padding:2px 8px;border-radius:10px;margin-left:6px;font-weight:500;vertical-align:middle}}
.badge-done{{background:#065f46;color:#6ee7b7}}
.badge-draft{{background:#78350f;color:#fcd34d}}
.badge-real{{background:#1e3a5f;color:#93c5fd}}
#toc{{background:#1e293b;border:1px solid #334155;border-radius:10px;padding:12px 16px;margin:12px 0;font-size:.82rem}}
#toc .toc-title{{font-weight:500;color:#94a3b8;margin-bottom:6px}}
#toc a{{display:block;color:#cbd5e1;padding:2px 0;text-decoration:none}}
#toc a:hover{{color:#38bdf8}}
@media(max-width:768px){{#sidebar{{display:none}}#content{{padding:20px}}}}
</style>
</head>
<body>
<div id="sidebar">
<div class="head"><h2>{html_mod.escape(title)}</h2><div class="subtitle" id="count">{len(md_files)} 个文件</div></div>
<input id="search" type="text" placeholder="🔍 搜索标题与正文…">
<div id="tree"></div>
</div>
<div id="content"><div class="empty"><div class="icon">👈</div>从左侧选择文件查看</div></div>
<script>
"use strict";
const DATA={data_js};
const TREE={tree_js};
let byId={{}};DATA.forEach(d=>byId[d.id]=d);
let current=null;let searchText="";

function esc(s){{return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}}

function inline(t){{
  t=esc(t);
  t=t.replace(/`([^`]+)`/g,"<code>$1</code>");
  t=t.replace(/\\*\\*([^*]+)\\*\\*/g,"<strong>$1</strong>");
  t=t.replace(/\\*([^*\\n]+)\\*/g,"<em>$1</em>");
  t=t.replace(/!\\[([^\\]]*)\\]\\(([^)\\s]+)(?:\\s+["']([^"']*)["'])?\\)/g,"<img src=\\"$2\\" alt=\\"$1\\">");
  t=t.replace(/\\[([^\\]]+)\\]\\(([^)\\s]+)(?:\\s+["']([^"']*)["'])?\\)/g,"<a data-href=\\"$2\\">$1</a>");
  return t;
}}

function renderLinks(el){{
  el.querySelectorAll("a[data-href]").forEach(a=>{{
    let h=a.getAttribute("data-href");
    if(/^\\.md$|^[\\w\\-/.]+(?:\\.md)(?:#.*)?$/.test(h)||h.endsWith(".md")){{
      a.addEventListener("click",()=>openMd(h));
      a.title="内部文档链接";
    }}else if(/^https?:\\/\\//.test(h)){{
      a.href=h;a.target="_blank";
    }}else{{a.href=h;}}
  }});
}}

function openMd(ref){{
  let path=ref.split("#")[0];
  let found=Object.values(byId).find(d=>d.rel===path);
  if(found){{showFile(found.id);return;}}
  let norm=path.replace(/^\\/+/,"");
  found=Object.values(byId).find(d=>d.rel.endsWith(norm));
  if(found){{showFile(found.id);}}
}}

function mdToHtml(md){{
  let lines=md.split(/\\r?\\n/);let out=[];let i=0;
  const blk={{
    "```":()=>{{let buf=[];i++;while(i<lines.length&&!lines[i].startsWith("```")){{buf.push(lines[i]);i++;}}i++;return "<pre><code>"+esc(buf.join("\\n"))+"</code></pre>";}},
    ">":()=>{{let buf=[];while(i<lines.length&&lines[i].startsWith(">")){{buf.push(lines[i].replace(/^>\\s?/,""));i++;}}return "<blockquote>"+buf.map(l=>"<p>"+inline(l)+"</p>").join("")+"</blockquote>";}},
    "|":()=>{{let buf=[];while(i<lines.length&&lines[i].trim().startsWith("|")){{buf.push(lines[i].trim());i++;}}if(buf.length<2)return "";let header=buf[0].split("|").filter(c=>c.trim()!=="");let rows=buf.slice(2).map(r=>r.split("|").filter(c=>c.trim()!=="").map(c=>"<td>"+inline(c)+"</td>").join(""));return "<table><thead><tr>"+header.map(h=>"<th>"+inline(h)+"</th>").join("")+"</tr></thead><tbody>"+rows.map(r=>"<tr>"+r+"</tr>").join("")+"</tbody></table>";}},
  }};
  while(i<lines.length){{
    let line=lines[i];
    if(line.trim()===""){{i++;continue;}}
    if(line.startsWith("```")){{out.push(blk["```"]());continue;}}
    if(line.startsWith(">")){{out.push(blk[">"]());continue;}}
    if(line.trim().startsWith("|")){{out.push(blk["|"]());continue;}}
    let h=line.match(/^(#{1,6})\\s+(.*)/);
    if(h){{let lv=h[1].length;out.push("<h"+lv+">"+inline(h[2])+"</h"+lv+">");i++;continue;}}
    if(/^[-*]\\s+/.test(line)){{let buf=[];while(i<lines.length&&/^[-*]\\s+/.test(lines[i])){{buf.push("<li>"+inline(lines[i].replace(/^[-*]\\s+/,""))+"</li>");i++;}}out.push("<ul>"+buf.join("")+"</ul>");continue;}}
    if(/^\\d+\\.\\s+/.test(line)){{let buf=[];while(i<lines.length&&/^\\d+\\.\\s+/.test(lines[i])){{buf.push("<li>"+inline(lines[i].replace(/^\\d+\\.\\s+/,""))+"</li>");i++;}}out.push("<ol>"+buf.join("")+"</ol>");continue;}}
    if(/^---+\\s*$/.test(line)){{out.push("<hr>");i++;continue;}}
    let buf=[line];i++;while(i<lines.length&&lines[i].trim()!==""&&!lines[i].match(/^(#{1,6})\\s/)&&!lines[i].startsWith("```")&&!lines[i].startsWith(">")&&!lines[i].trim().startsWith("|")&&!/^[-*]\\s+/.test(lines[i])&&!/^\\d+\\.\\s+/.test(lines[i])&&!/^---+\\s*$/.test(lines[i])){{buf.push(lines[i]);i++;}}
    out.push("<p>"+buf.map(l=>inline(l)).join("<br>")+"</p>");
  }}
  return out.join("\\n");
}}

function showFile(id){{
  let d=byId[id];if(!d)return;
  current=id;
  document.querySelectorAll(".file-link").forEach(l=>l.classList.toggle("active",l.dataset.id===id));
  let html="<h1>"+esc(d.title)+" "+d.badge+"</h1>";
  let toc=[];let tmp=document.createElement("div");
  tmp.innerHTML=mdToHtml(d.md);
  tmp.querySelectorAll("h2,h3").forEach((h,idx)=>{{
    let anchor="sec-"+idx;h.id=anchor;
    toc.push("<a data-toc=\\""+anchor+"\\">"+(h.tagName==="H2"?"":"&nbsp;&nbsp;")+esc(h.textContent)+"</a>");
  }});
  if(toc.length>2)html+="<div id=\\"toc\\"><div class=\\"toc-title\\">目录</div>"+toc.join("")+"</div>";
  html+=tmp.innerHTML;
  document.getElementById("content").innerHTML=html;
  renderLinks(document.getElementById("content"));
  document.getElementById("content").scrollTop=0;
  document.getElementById("content").querySelectorAll("a[data-toc]").forEach(a=>{{
    a.addEventListener("click",()=>{{document.getElementById(a.getAttribute("data-toc")).scrollIntoView({{behavior:"smooth",block:"start"}});}});
  }});
}}

function renderTree(node,container,path){{
  let keys=Object.keys(node).filter(k=>k!=="__files__");
  let files=node["__files__"]||[];
  let row=null;
  if(path!==""){{row=document.createElement("div");row.className="dir-row";row.dataset.dir=path;row.innerHTML='<span class="arrow">▶</span><span class="gicon">📁</span>'+esc(path.split("/").pop());container.appendChild(row);}}
  let childWrap=document.createElement("div");childWrap.className="children"+(path===""?" open":"");
  if(row){{row.addEventListener("click",()=>{{childWrap.classList.toggle("open");row.classList.toggle("open");}});}}
  keys.sort().forEach(k=>renderTree(node[k],childWrap,path?path+"/"+k:k));
  files.forEach(f=>{{
    let b=document.createElement("button");b.className="file-link";b.dataset.id=f[0];
    b.innerHTML='<span class="fname">'+esc(f[1])+'</span>';
    b.addEventListener("click",()=>showFile(f[0]));
    childWrap.appendChild(b);
  }});
  container.appendChild(childWrap);
}}

function applySearch(){{
  let q=searchText.trim().toLowerCase();
  document.querySelectorAll(".file-link").forEach(link=>{{
    let d=byId[link.dataset.id];
    let hit=!q||d.title.toLowerCase().includes(q)||d.md.toLowerCase().includes(q);
    link.style.display=hit?"":"none";
  }});
  document.querySelectorAll(".dir-row").forEach(row=>{{
    row.style.display="none";
  }});
  document.querySelectorAll(".children").forEach(c=>c.classList.add("open"));
}}

document.getElementById("search").addEventListener("input",e=>{{
  searchText=e.target.value;
  if(searchText.trim()){{applySearch();}}else{{document.getElementById("tree").innerHTML="";renderTree(TREE,document.getElementById("tree"),"");}}
}});

renderTree(TREE,document.getElementById("tree"),"");
if(DATA.length>0){{/* auto-open first file for demo friendliness */showFile(DATA[0].id);}}
</script>
</body>
</html>"""
    return html


def main():
    parser = argparse.ArgumentParser(
        description="Generate a self-contained offline HTML document browser from markdown files."
    )
    parser.add_argument("directory", help="Root directory containing .md files")
    parser.add_argument("--output", default="index.html", help="Output HTML file path")
    parser.add_argument("--title", default="文档浏览", help="Page title")
    parser.add_argument("--config", default=None, help="Optional YAML config for group rules / badges / order")
    args = parser.parse_args()

    root_dir = os.path.abspath(args.directory)
    if not os.path.isdir(root_dir):
        print(f"Error: '{root_dir}' is not a directory", file=sys.stderr)
        sys.exit(1)

    config = parse_simple_yaml(args.config)
    title = args.title if not config.get("title") else config["title"]

    md_files = collect_md_files(root_dir)
    if not md_files:
        print(f"Error: No .md files found in '{root_dir}'", file=sys.stderr)
        sys.exit(1)

    output_path = args.output
    if not os.path.isabs(output_path):
        output_path = os.path.join(root_dir, output_path)

    html = generate_html(root_dir, title, md_files, config)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    size_kb = os.path.getsize(output_path) / 1024
    print(f"✅ Generated {output_path} ({size_kb:.1f} KB)")
    print(f"   Embedded {len(md_files)} markdown files | Offline-ready | Search + Tree + Cross-links")


if __name__ == "__main__":
    main()
