#!/usr/bin/env python3
"""
Nomic Atlas 记忆可视化器 - 语义嵌入版
=====================================
读取 memory-tdai 的 L1 记忆记录，用真正的语义嵌入模型生成向量，
UMAP 降维后输出交互式 HTML 可视化页面。

嵌入方案优先级:
1. sentence-transformers (nomic-embed-text-v1.5) — 768 维语义向量
2. TF-IDF 回退 — 当模型加载失败时使用

输出:
- output/memory_visualization.html — 交互式可视化页面
- memory/nomic_atlas_integration_YYYY-MM-DD.md — 总结报告
"""

import sqlite3
import json
import os
import sys
from datetime import datetime

# Fix Windows console encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Paths
DB_PATH = r"D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\memory-tdai\vectors.db"
OUTPUT_DIR = r"D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\output"
REPORT_PATH = r"D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\memory"

# GGUF model path (kept for reference; not used directly since sentence-transformers handles HF format)
GGUF_MODEL_PATH = r"D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\models\nomic-embed-text-v1.5.Q4_K_M.gguf"


def load_records():
    """从 vectors.db 加载所有 L1 记忆记录"""
    if not os.path.exists(DB_PATH):
        print(f"❌ 数据库不存在: {DB_PATH}")
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM l1_records ORDER BY created_time")
    records = [dict(row) for row in cursor.fetchall()]
    conn.close()
    print(f"✅ 加载 {len(records)} 条 L1 记忆记录")
    return records


def generate_embeddings_sentence_transformers(contents, model_name="nomic-ai/nomic-embed-text-v1.5"):
    """方案 1: 使用 sentence-transformers 生成 768 维语义嵌入"""
    try:
        from sentence_transformers import SentenceTransformer
        import numpy as np

        print(f"🔄 加载语义嵌入模型: {model_name}")
        print("   (首次运行需下载模型 ~274MB，之后使用本地缓存)")
        model = SentenceTransformer(model_name, trust_remote_code=True)

        print("🔄 生成语义嵌入向量...")
        embeddings = model.encode(
            contents,
            batch_size=16,
            show_progress_bar=True,
            convert_to_numpy=True,
        )

        print(f"✅ 语义嵌入维度: {embeddings.shape}")
        return embeddings, "sentence-transformers"

    except Exception as e:
        print(f"⚠️  语义嵌入模型加载失败: {e}")
        return None, None


def generate_embeddings_tfidf(contents):
    """方案 2 (回退): TF-IDF 向量"""
    from sklearn.feature_extraction.text import TfidfVectorizer
    import numpy as np

    print("🔧 使用 TF-IDF 回退方案...")
    vectorizer = TfidfVectorizer(
        max_features=100,
        ngram_range=(1, 2),
        min_df=1,
    )
    tfidf_matrix = vectorizer.fit_transform(contents)
    embeddings = tfidf_matrix.toarray()
    print(f"✅ TF-IDF 矩阵: {embeddings.shape}")
    return embeddings, "TF-IDF"


def reduce_to_2d(embeddings, n_samples):
    """UMAP 降维到 2D"""
    try:
        import umap
        use_umap = True
    except ImportError:
        use_umap = False
        print("⚠️  umap-learn 未安装，使用 PCA 替代")
        from sklearn.decomposition import PCA

    if use_umap:
        n_neighbors = min(5, max(2, n_samples - 1))
        reducer = umap.UMAP(
            n_components=2,
            n_neighbors=n_neighbors,
            min_dist=0.1,
            random_state=42,
            metric="cosine",
        )
        embedding_2d = reducer.fit_transform(embeddings)
        method_name = "UMAP"
    else:
        reducer = PCA(n_components=2, random_state=42)
        embedding_2d = reducer.fit_transform(embeddings)
        method_name = "PCA"

    print(f"✅ {method_name} 降维完成: {embedding_2d.shape}")
    return embedding_2d, method_name


def generate_local_visualization(records):
    """生成嵌入 + UMAP 降维 + Plotly HTML"""
    contents = [r["content"] for r in records]

    # 尝试语义嵌入
    embeddings, embed_method = generate_embeddings_sentence_transformers(contents)

    # 回退到 TF-IDF
    if embeddings is None:
        embeddings, embed_method = generate_embeddings_tfidf(contents)

    # 降维
    embedding_2d, reduce_method = reduce_to_2d(embeddings, len(records))

    # 类型颜色映射
    type_colors = {
        "persona": "#FF6B6B",      # 红色
        "episodic": "#4ECDC4",     # 青色
        "instruction": "#45B7D1",  # 蓝色
    }

    # 生成 HTML
    html = generate_html(records, embedding_2d, type_colors, reduce_method, embed_method)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "memory_visualization.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n✅ 可视化页面已保存: {output_path}")
    return output_path, embed_method, reduce_method


def generate_html(records, embedding_2d, type_colors, method_name, embed_method):
    """生成交互式 HTML 可视化页面"""

    # 构建数据 JSON
    data_points = []
    for i, r in enumerate(records):
        data_points.append({
            "id": r["record_id"],
            "content": r["content"],
            "type": r["type"],
            "priority": r["priority"],
            "scene_name": r["scene_name"],
            "timestamp": r["timestamp_str"],
            "created_time": r["created_time"],
            "x": float(embedding_2d[i][0]),
            "y": float(embedding_2d[i][1]),
            "color": type_colors.get(r["type"], "#999999"),
        })

    data_json = json.dumps(data_points, ensure_ascii=False, indent=2)

    embed_label = "语义嵌入 (nomic-embed-text)" if "sentence" in embed_method.lower() else embed_method

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenClaw L1 记忆可视化 - 语义嵌入</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans SC', sans-serif;
            background: #0a0a1a;
            color: #e0e0e0;
            overflow: hidden;
        }}
        #header {{
            position: fixed;
            top: 0; left: 0; right: 0;
            height: 56px;
            background: rgba(10, 10, 26, 0.95);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255,255,255,0.1);
            display: flex;
            align-items: center;
            padding: 0 24px;
            z-index: 100;
        }}
        #header h1 {{
            font-size: 18px;
            font-weight: 600;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        #header .stats {{ margin-left: auto; font-size: 13px; color: #888; }}
        #canvas {{ position: fixed; top: 56px; left: 0; right: 0; bottom: 0; }}
        .point {{
            position: absolute;
            width: 20px; height: 20px;
            border-radius: 50%;
            cursor: pointer;
            transform: translate(-50%, -50%);
            transition: transform 0.2s, box-shadow 0.2s;
            border: 2px solid rgba(255,255,255,0.3);
        }}
        .point:hover {{
            transform: translate(-50%, -50%) scale(1.5);
            box-shadow: 0 0 20px rgba(255,255,255,0.5);
            z-index: 50;
        }}
        .point .label {{
            position: absolute; top: 24px; left: 50%;
            transform: translateX(-50%);
            font-size: 10px; white-space: nowrap;
            color: #aaa; opacity: 0;
            transition: opacity 0.2s; pointer-events: none;
        }}
        .point:hover .label {{ opacity: 1; }}
        #detail {{
            position: fixed; right: 0; top: 56px;
            width: 420px; height: calc(100% - 56px);
            background: rgba(15, 15, 35, 0.98);
            backdrop-filter: blur(20px);
            border-left: 1px solid rgba(255,255,255,0.1);
            padding: 24px;
            transform: translateX(100%);
            transition: transform 0.3s ease;
            z-index: 90; overflow-y: auto;
        }}
        #detail.open {{ transform: translateX(0); }}
        #detail .close-btn {{
            position: absolute; top: 16px; right: 16px;
            width: 32px; height: 32px; border-radius: 50%;
            background: rgba(255,255,255,0.1); border: none;
            color: #fff; cursor: pointer; font-size: 18px;
            display: flex; align-items: center; justify-content: center;
        }}
        #detail .close-btn:hover {{ background: rgba(255,255,255,0.2); }}
        #detail h2 {{ font-size: 16px; margin-bottom: 16px; padding-right: 40px; color: #fff; }}
        #detail .meta {{
            display: grid; grid-template-columns: 80px 1fr;
            gap: 8px; font-size: 13px; margin-bottom: 16px;
        }}
        #detail .meta-label {{ color: #666; }}
        #detail .meta-value {{ color: #ccc; }}
        #detail .content {{
            background: rgba(255,255,255,0.05); border-radius: 8px;
            padding: 16px; font-size: 14px; line-height: 1.6;
            color: #ddd; margin-top: 16px;
        }}
        #legend {{
            position: fixed; bottom: 24px; left: 24px;
            background: rgba(10, 10, 26, 0.9);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px; padding: 16px; z-index: 80;
        }}
        #legend h3 {{ font-size: 13px; color: #888; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px; }}
        .legend-item {{
            display: flex; align-items: center; gap: 8px;
            margin-bottom: 8px; font-size: 14px; cursor: pointer;
            padding: 4px 8px; border-radius: 6px; transition: background 0.2s;
        }}
        .legend-item:hover {{ background: rgba(255,255,255,0.1); }}
        .legend-item.dimmed {{ opacity: 0.3; }}
        .legend-dot {{ width: 12px; height: 12px; border-radius: 50%; }}
        #filter {{
            position: fixed; bottom: 24px; left: 200px;
            background: rgba(10, 10, 26, 0.9);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px; padding: 16px; z-index: 80;
        }}
        #filter h3 {{ font-size: 13px; color: #888; margin-bottom: 8px; }}
        #filter input {{
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 6px; padding: 8px 12px;
            color: #fff; font-size: 13px; width: 200px; outline: none;
        }}
        #filter input:focus {{ border-color: #667eea; }}
        .tooltip {{
            position: fixed;
            background: rgba(20, 20, 40, 0.95);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 8px; padding: 12px 16px;
            font-size: 13px; max-width: 300px;
            pointer-events: none; z-index: 200;
            display: none; box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }}
        #cluster-info {{
            position: fixed; top: 70px; right: 24px;
            background: rgba(10, 10, 26, 0.9);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px; padding: 16px;
            z-index: 80; max-width: 280px;
        }}
        #cluster-info h3 {{ font-size: 13px; color: #888; margin-bottom: 10px; }}
        #cluster-info .cluster {{
            font-size: 12px; color: #bbb; margin-bottom: 6px;
            padding: 4px 8px; background: rgba(255,255,255,0.05);
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div id="header">
        <h1>🧠 OpenClaw L1 记忆可视化</h1>
        <div class="stats">{embed_label} · {method_name} 降维 · {len(records)} 条记忆</div>
    </div>

    <div id="canvas"></div>

    <div id="legend">
        <h3>记忆类型</h3>
        <div class="legend-item" data-type="persona">
            <div class="legend-dot" style="background: {type_colors['persona']}"></div>
            <span>Persona ({sum(1 for r in records if r['type']=='persona')})</span>
        </div>
        <div class="legend-item" data-type="episodic">
            <div class="legend-dot" style="background: {type_colors['episodic']}"></div>
            <span>Episodic ({sum(1 for r in records if r['type']=='episodic')})</span>
        </div>
        <div class="legend-item" data-type="instruction">
            <div class="legend-dot" style="background: {type_colors['instruction']}"></div>
            <span>Instruction ({sum(1 for r in records if r['type']=='instruction')})</span>
        </div>
    </div>

    <div id="filter">
        <h3>搜索记忆</h3>
        <input type="text" id="searchInput" placeholder="输入关键词搜索...">
    </div>

    <div id="detail">
        <button class="close-btn" onclick="closeDetail()">×</button>
        <div id="detailContent"></div>
    </div>

    <div class="tooltip" id="tooltip"></div>

    <script>
        const data = {data_json};

        let scale = 1, offsetX = 0, offsetY = 0;
        let isDragging = false, dragStartX, dragStartY;

        const xs = data.map(d => d.x);
        const ys = data.map(d => d.y);
        const minX = Math.min(...xs), maxX = Math.max(...xs);
        const minY = Math.min(...ys), maxY = Math.max(...ys);
        const rangeX = maxX - minX || 1;
        const rangeY = maxY - minY || 1;

        function renderPoints() {{
            const canvas = document.getElementById('canvas');
            canvas.innerHTML = '';
            const w = canvas.clientWidth, h = canvas.clientHeight;
            const padding = 80;

            data.forEach(d => {{
                const px = padding + ((d.x - minX) / rangeX) * (w - 2 * padding);
                const py = padding + ((d.y - minY) / rangeY) * (h - 2 * padding);

                const el = document.createElement('div');
                el.className = 'point';
                el.dataset.type = d.type;
                el.dataset.id = d.id;
                el.style.left = px + 'px';
                el.style.top = py + 'px';
                el.style.background = d.color;
                el.style.boxShadow = `0 0 12px ${{d.color}}40`;

                const label = document.createElement('div');
                label.className = 'label';
                label.textContent = d.scene_name.length > 15 ? d.scene_name.slice(0, 15) + '...' : d.scene_name;
                el.appendChild(label);

                el.addEventListener('click', () => showDetail(d));
                el.addEventListener('mouseenter', (e) => showTooltip(e, d));
                el.addEventListener('mouseleave', hideTooltip);

                canvas.appendChild(el);
            }});
        }}

        function showDetail(d) {{
            const detail = document.getElementById('detail');
            const content = document.getElementById('detailContent');
            const typeLabels = {{persona: '👤 Persona', episodic: '📅 Episodic', instruction: '📋 Instruction'}};
            content.innerHTML = `
                <h2>${{typeLabels[d.type] || d.type}}</h2>
                <div class="meta">
                    <span class="meta-label">ID</span>
                    <span class="meta-value" style="font-size:11px">${{d.id}}</span>
                    <span class="meta-label">场景</span>
                    <span class="meta-value">${{d.scene_name}}</span>
                    <span class="meta-label">优先级</span>
                    <span class="meta-value">${{'🔴'.repeat(Math.min(d.priority, 5))}} (${{d.priority}}/10)</span>
                    <span class="meta-label">时间</span>
                    <span class="meta-value">${{d.timestamp}}</span>
                    <span class="meta-label">创建</span>
                    <span class="meta-value">${{d.created_time}}</span>
                </div>
                <div class="content">${{d.content}}</div>
            `;
            detail.classList.add('open');
        }}

        function closeDetail() {{
            document.getElementById('detail').classList.remove('open');
        }}

        function showTooltip(e, d) {{
            const tooltip = document.getElementById('tooltip');
            tooltip.style.display = 'block';
            tooltip.style.left = (e.clientX + 16) + 'px';
            tooltip.style.top = (e.clientY - 10) + 'px';
            tooltip.innerHTML = `<strong>${{d.scene_name}}</strong><br><span style="color:#888;font-size:12px">${{d.content.slice(0, 80)}}...</span>`;
        }}

        function hideTooltip() {{
            document.getElementById('tooltip').style.display = 'none';
        }}

        document.querySelectorAll('.legend-item').forEach(item => {{
            item.addEventListener('click', () => {{
                const type = item.dataset.type;
                item.classList.toggle('dimmed');
                const isDimmed = item.classList.contains('dimmed');
                document.querySelectorAll(`.point[data-type="${{type}}"]`).forEach(p => {{
                    p.style.opacity = isDimmed ? '0.15' : '1';
                }});
            }});
        }});

        document.getElementById('searchInput').addEventListener('input', (e) => {{
            const query = e.target.value.toLowerCase();
            document.querySelectorAll('.point').forEach(p => {{
                const d = data.find(d => d.id === p.dataset.id);
                const match = !query || d.content.toLowerCase().includes(query) || d.scene_name.toLowerCase().includes(query);
                p.style.opacity = match ? '1' : '0.15';
            }});
        }});

        renderPoints();
        window.addEventListener('resize', renderPoints);

        function drawConnections() {{
            const canvas = document.getElementById('canvas');
            const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            svg.style.cssText = 'position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:1;';
            svg.id = 'connections';
            canvas.insertBefore(svg, canvas.firstChild);

            const points = document.querySelectorAll('.point');
            const positions = [];
            points.forEach(p => {{
                positions.push({{ id: p.dataset.id, x: parseFloat(p.style.left), y: parseFloat(p.style.top) }});
            }});

            const sceneGroups = {{}};
            data.forEach(d => {{
                if (!sceneGroups[d.scene_name]) sceneGroups[d.scene_name] = [];
                sceneGroups[d.scene_name].push(d);
            }});

            Object.entries(sceneGroups).forEach(([scene, members]) => {{
                if (members.length > 1) {{
                    for (let i = 0; i < members.length; i++) {{
                        for (let j = i + 1; j < members.length; j++) {{
                            const p1 = positions.find(p => p.id === members[i].id);
                            const p2 = positions.find(p => p.id === members[j].id);
                            if (p1 && p2) {{
                                const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                                line.setAttribute('x1', p1.x);
                                line.setAttribute('y1', p1.y);
                                line.setAttribute('x2', p2.x);
                                line.setAttribute('y2', p2.y);
                                line.setAttribute('stroke', 'rgba(255,255,255,0.15)');
                                line.setAttribute('stroke-width', '1');
                                line.setAttribute('stroke-dasharray', '4,4');
                                svg.appendChild(line);
                            }}
                        }}
                    }}
                }}
            }});
        }}

        setTimeout(drawConnections, 100);
    </script>
</body>
</html>"""

    return html


def write_report(output_path, method_name, record_count, records, embed_method):
    """生成总结报告"""
    os.makedirs(REPORT_PATH, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = os.path.join(REPORT_PATH, f"nomic_atlas_integration_{today}.md")

    embed_label = "语义嵌入 (nomic-embed-text-v1.5)" if "sentence" in embed_method.lower() else embed_method

    type_counts = {}
    for r in records:
        type_counts[r["type"]] = type_counts.get(r["type"], 0) + 1

    type_rows = ""
    for t, c in sorted(type_counts.items()):
        type_rows += f"| {t} | {c} | {c/record_count*100:.0f}% |\n"

    scene_counts = {}
    for r in records:
        s = r.get("scene_name", "unknown")
        scene_counts[s] = scene_counts.get(s, 0) + 1
    top_scenes = sorted(scene_counts.items(), key=lambda x: -x[1])[:5]
    scene_rows = ""
    for s, c in top_scenes:
        scene_rows += f"| {s} | {c} |\n"

    report = f"""# Nomic Atlas 记忆可视化报告

**日期**: {today}
**状态**: ✅ 完成

## 嵌入方案

| 方案 | 状态 | 说明 |
|------|------|------|
| 语义嵌入 (sentence-transformers) | {'✅ 成功' if 'sentence' in embed_method.lower() else '❌ 回退'} | {embed_label} |
| TF-IDF 回退 | {'跳过' if 'sentence' in embed_method.lower() else '✅ 使用'} | 最大 100 维 |

**实际使用**: {embed_label}

## 数据处理

- **数据源**: `memory-tdai/vectors.db` (l1_records 表)
- **记录数**: {record_count} 条
- **嵌入方式**: {embed_label}
- **降维方式**: {method_name} (2D)
- **可视化**: 纯 HTML + CSS + JavaScript

## 可视化输出

- **HTML 路径**: `{output_path}`

## 记忆分布

| 类型 | 数量 | 占比 |
|------|------|------|
{type_rows}

## Top 场景

| 场景 | 记录数 |
|------|--------|
{scene_rows}
"""

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n📝 报告已保存: {report_path}")
    return report_path


if __name__ == "__main__":
    print("=" * 60)
    print("🧠 OpenClaw L1 记忆可视化 - 语义嵌入版")
    print("=" * 60)

    # Step 1: 加载数据
    records = load_records()

    if not records:
        print("❌ 没有找到记忆记录")
        sys.exit(1)

    # Step 2: 生成嵌入 + 可视化
    output_path, embed_method, reduce_method = generate_local_visualization(records)

    # Step 3: 写报告
    write_report(output_path, reduce_method, len(records), records, embed_method)

    print("\n" + "=" * 60)
    print("✅ 完成!")
    print(f"📄 HTML: {output_path}")
    print("=" * 60)
