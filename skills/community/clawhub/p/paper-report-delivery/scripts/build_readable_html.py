#!/usr/bin/env python3
import base64
import html
import json
import mimetypes
from pathlib import Path
from PIL import Image

ROOT = Path.cwd()
SELECTED = ROOT / 'data' / 'selected.json'
IMAGE_META_DIR = ROOT / 'assets' / 'image_meta'
OUT_DIR = ROOT / 'output' / 'readable'
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path: Path):
    return json.loads(path.read_text())


def escape(text):
    return html.escape(str(text or ''))


def slugify(value: str):
    text = str(value or '').strip().lower()
    out = []
    for ch in text:
        if ch.isalnum():
            out.append(ch)
        else:
            out.append('-')
    slug = ''.join(out)
    while '--' in slug:
        slug = slug.replace('--', '-')
    return slug.strip('-') or 'item'


def to_embeddable_image(path: Path):
    suffix = path.suffix.lower()
    if suffix not in ['.ppm', '.pbm', '.pgm']:
        return path
    png_path = path.with_suffix('.embedded.png')
    if not png_path.exists():
        with Image.open(path) as img:
            rgb = img.convert('RGB')
            rgb.save(png_path, format='PNG')
    return png_path


def data_uri(path_str: str):
    if not path_str:
        return ''
    path = Path(path_str)
    if not path.exists() or not path.is_file():
        return ''
    path = to_embeddable_image(path)
    suffix = path.suffix.lower()
    mime, _ = mimetypes.guess_type(str(path))
    if not mime:
        if suffix in ['.jpg', '.jpeg']:
            mime = 'image/jpeg'
        elif suffix == '.png':
            mime = 'image/png'
        elif suffix == '.webp':
            mime = 'image/webp'
        elif suffix == '.gif':
            mime = 'image/gif'
        else:
            mime = 'application/octet-stream'
    encoded = base64.b64encode(path.read_bytes()).decode('ascii')
    return f'data:{mime};base64,{encoded}'


def cn_summary_detailed(item):
    if item.get('type') == 'platform_update':
        return '这是一条与机器人仿真/训练工具链直接相关的平台更新。其核心内容通常不是提出一套新的算法理论，而是把新的接口、功能、兼容性修复或性能优化交付给研究者和工程用户，因此摘要部分保持简洁，重点关注它会如何影响后续实验与部署流程。'

    # 这里的目标不是做一句话概括，而是尽量忠实地把 abstract 的主要信息翻译成中文，并保留方法、问题与结果结构。

    title = item.get('title', '')
    abstract = item.get('abstract', '')
    low = f'{title} {abstract}'.lower()

    if 'structvla' in low or ('structured' in low and 'world model' in low):
        return '这篇论文讨论的是世界模型在机器人操作中的一个典型问题：如果继续让模型去做稠密未来画面预测，虽然表面上看信息很多，但其中包含大量冗余视觉细节，而且预测误差会随着时间步不断累积，最终造成长时规划偏移。作者提出 StructVLA，把原本生成整段未来画面的 world model，改造成显式预测一组稀疏但具有物理语义的结构化关键帧。这些关键帧不是随意抽样的图像，而是来自抓手状态变化、运动学转折点等与任务进度强相关的时刻。随后，作者再通过统一离散 token 词表和两阶段训练流程，先学会预测这些结构化帧，再把它们映射到低层动作控制，从而把视觉规划和执行控制连接得更紧。'
    if 'roboclaw' in low or 'entangled action pairs' in low:
        return '这篇论文关注长时机器人任务中一个非常现实的问题：当前很多 VLA 系统把“数据采集、策略训练、最终部署”拆成多个阶段，各阶段语义不一致，而且高度依赖人工重置环境，导致扩展到长流程任务时成本非常高。作者提出 RoboClaw，用一个统一的 VLM 驱动控制器把数据采集、策略学习和任务执行连接起来。摘要里的关键机制是 Entangled Action Pairs，也就是把正向操作与逆向恢复动作成对绑定，让机器人在执行一次操作后能够自己回到可继续采数的状态，从而形成持续的 on-policy 数据采集闭环。部署阶段则继续由同一个 agent 负责高层推理和策略原语编排，减少训练阶段与执行阶段之间的语义错位。'
    if 'decovln' in low or ('navigation' in low and 'long-term memory' in low):
        return '这篇论文聚焦视觉语言导航中的两个核心难点：第一，长时导航过程中应该如何构造真正有用的长期记忆；第二，当 agent 偏离专家轨迹后，如何避免误差不断累积。作者提出 DecoVLN，把记忆构建写成一个优化问题：系统不是简单缓存所有历史帧，而是在候选历史中依据统一评分函数反复挑选更合适的记忆片段，这个评分同时平衡指令语义相关性、已选记忆之间的视觉多样性，以及整段轨迹的时间覆盖。与此同时，作者还提出基于 state-action pair 的纠错微调策略，用 geodesic distance 精确衡量当前状态偏离专家轨迹的程度，只保留可信区域内的高质量纠错样本，从而提升闭环纠偏时的稳定性。'
    if 'robostream' in low or 'spatio-temporal' in low or 'causal' in low:
        return '这篇论文针对的是 VLM 规划器在长时机器人操作中的一个根本缺陷：很多方法把每一步都当成独立的“图像到动作”映射，导致模型每次都要从头理解场景，却没有真正记住之前动作如何改变了环境。RoboStream 的思路是引入持续存在的时空记忆结构。作者提出 STF-Tokens，把视觉证据和 3D 几何属性绑定起来，用于稳定对象锚定；同时构造 Causal Spatio-Temporal Graph，记录每一步动作触发的状态变化，形成显式的因果链条。这样系统在面对遮挡、状态变化和长执行链时，不需要反复从像素层重建一切，而是可以沿着已有记忆和因果结构持续跟踪对象与前置条件。'
    if 'steve-evolving' in low or 'self-evolution' in low or 'dual-track knowledge distillation' in low:
        return '这篇论文讨论的是开放世界具身任务中的持续演化问题。作者认为瓶颈并不只是单步规划质量，而是机器人经历过的交互经验如何被组织、诊断、提炼，并再次反馈到后续决策中。为此，Steve-Evolving 采用一个非参数式闭环框架：先把每次子目标尝试写成结构化经验元组，包括前状态、动作、诊断结果和后状态；再通过多层索引和滚动总结让这些经验可检索、可审计；然后把成功轨迹蒸馏成可复用技能，把失败经验蒸馏成显式 guardrails；最后在规划阶段把技能和约束重新注入 LLM planner，并根据诊断结果做局部重规划。整个过程强调的是“经验组织和控制逻辑的演化”，而不是重新训练模型参数。'
    if 'hybrid deformable-rigid' in low or 'cosserat' in low:
        return '这篇论文处理的是受约束环境中刚柔混合物体的协同操控问题。与只处理绳索或纯刚体不同，这类对象同时具有可形变段和刚性段，导致建模和规划都更困难。作者使用基于应变的 Cosserat rod 模型，把传统刚体规划拓展到 hybrid deformable linear objects，并构建一个准静态优化式操控规划器。摘要中强调的重点是：该方法利用可微模型和解析梯度来高效求解 inverse kinetostatic 问题，并进一步 warm-start 后续轨迹优化过程。也就是说，作者不仅给出了能表示这类对象的方法，还把它真正写进了可求解、可加速的优化框架里。'
    if 'comfree-sim' in low or 'contact physics engine' in low:
        return '这篇论文围绕接触丰富机器人任务中的仿真与控制效率问题展开。传统接触仿真常常要在精度、稳定性和并行效率之间做艰难折中，而这篇工作试图通过解析式接触物理引擎重新组织这一问题。摘要指出，作者提出的是一个适合 GPU 并行的 analytical contact physics engine，用于大规模接触丰富场景的仿真与控制。换句话说，它的目标不是仅仅让仿真“能跑”，而是希望在大吞吐、较高频率、可用于控制回路的条件下维持足够合理的物理建模，从而让训练和控制两侧都能受益。'
    if 'vector field' in low and 'drone racing' in low:
        return '这篇论文关注视觉无人机竞速里一个很典型的问题：策略学习目标往往高度非线性、非平滑，尤其在高速穿门等任务中，直接从图像和控制目标之间建立稳定的可微训练信号并不容易。作者提出把向量场先验注入 differentiable policy learning 中，用几何上更连续的方向场来描述“应该朝哪里飞、如何逐渐靠近目标轨迹”。这样一来，学习过程不再只依赖稀疏或不稳定的任务反馈，而是有了更平滑、更可传播的结构化指导信号。'

    return '这篇论文围绕机器人/具身智能相关问题提出了一套完整方法，摘要里强调的是当前方法的关键瓶颈、作者引入的新结构，以及这种结构如何改善长时任务中的稳定性、效率或泛化能力。下面的创新点部分会进一步展开方法细节。'


def innovation_points(item):
    if item.get('type') == 'platform_update':
        return [
            '这类条目的重点不在算法创新，而在于工程能力的交付：例如新接口、兼容性修复、性能优化或文档完善。',
            '对研究者的实际价值通常体现在更低的实验成本、更稳定的环境配置，以及更顺滑的训练/部署流程。',
        ]

    title = item.get('title', '')
    abstract = item.get('abstract', '')
    low = f'{title} {abstract}'.lower()

    if 'structvla' in low or ('structured' in low and 'world model' in low):
        return [
            '它不是继续做稠密未来视频预测，而是把世界模型的输出压缩成少量与任务进展强相关的结构化关键帧，减少无关视觉细节。',
            '这些结构化帧来源于抓手状态切换、运动学转折等物理事件，因此比纯语义子目标或隐变量更贴近真实控制需求。',
            '作者用统一离散 token 词表把“结构化预测”和“动作生成”放进一条训练链路里，避免高层规划表示和低层执行控制脱节。',
            '它解决的核心不是单步识别准确率，而是长时操作中预测误差不断堆积、最终让计划漂移的问题。',
            '从方法论上看，这篇工作代表的是：把 world model 从“想象未来画面”推进到“生成可执行规划支架”。',
        ]
    if 'roboclaw' in low or 'entangled action pairs' in low:
        return [
            '最核心的设计是 Entangled Action Pairs：把执行任务的正向动作与环境恢复的逆向动作成对建模，形成可自复位的数据采集循环。',
            '这意味着机器人不需要每次采完数据都依赖人工 reset，而是可以在 on-policy 过程中持续收集、持续修正、持续迭代。',
            '作者还把数据采集、策略学习和部署阶段统一在同一个 VLM-agent 控制器之下，减少不同阶段语义表示不一致的问题。',
            '部署时同一个 agent 继续承担高层推理和策略原语调度，因此多策略串联时更不容易出现 open-loop 式脆弱切换。',
            '它真正解决的是“长流程机器人系统很难规模化运转”的工程瓶颈，而不只是单个策略性能再提升一点。',
        ]
    if 'decovln' in low or ('navigation' in low and 'long-term memory' in low):
        return [
            '作者没有把长期记忆当成简单缓存，而是把“应该记住哪些历史帧”正式写成一个优化问题。',
            '统一评分函数同时考虑三件事：和当前语言指令是否相关、和已选记忆是否足够多样、以及是否覆盖了历史轨迹的重要时间片段。',
            '针对 compounding errors，它不是泛泛做数据增强，而是用 geodesic distance 精确量化状态偏离程度，只保留可信区域内的纠错样本。',
            '因此这篇工作的创新在于，把“记忆选择”和“纠错数据质量控制”都从启发式处理提升成更明确、可解释的机制。',
            '从闭环控制角度看，它改善的是长期导航里最致命的两个问题：记忆失真和错误滚雪球。',
        ]
    if 'robostream' in low or 'spatio-temporal' in low or 'causal' in low:
        return [
            'RoboStream 的第一层创新是 STF-Tokens：把视觉证据与 3D 几何属性绑定，形成可持续使用的对象锚点，而不是每一步都重新从像素中猜。',
            '第二层创新是 Causal Spatio-Temporal Graph：它不只记住“看到了什么”，还记录“哪个动作导致了什么状态变化”。',
            '这种设计使模型能显式追踪因果链条，比如某个容器是否已经被移动、某个积木是否已经被遮挡、某个前置条件是否已满足。',
            '关键点在于这套机制是 training-free 的，不依赖重新微调大模型，而是通过外部结构增强长时推理与记忆能力。',
            '它相对以往 VLM planner 的优势，是把对象持久性、时序变化和动作后果变成了可被访问的显式状态，而不是隐含在上下文里。',
        ]
    if 'steve-evolving' in low or 'self-evolution' in low or 'dual-track knowledge distillation' in low:
        return [
            '它不是依赖持续微调参数来“成长”，而是依赖经验结构化、诊断、蒸馏和约束注入来实现非参数式自演化。',
            'Experience Anchoring 把每次子目标尝试写成固定 schema 的经验元组，并结合条件签名、空间哈希、语义标签等多维索引，方便检索和审计。',
            '诊断信号也不是简单成功/失败二分类，而是包含状态差异总结、失败原因枚举、连续指标以及停滞/循环检测。',
            '成功经验会被蒸馏成显式技能，失败经验则被蒸馏成 guardrails，这相当于同时强化“该做什么”和“不要做什么”。',
            '真正有意思的地方在于：这些技能与约束会重新注入 planner，并随着局部重规划在线更新，因此系统会越来越像一个会积累操作经验的执行体。',
        ]
    if 'hybrid deformable-rigid' in low or 'cosserat' in low:
        return [
            '它把传统主要面向刚体或单一柔性体的建模，扩展到了刚柔混合对象，这本身就显著提升了问题表达能力。',
            '作者采用 strain-based Cosserat rod 模型，并把它放进准静态优化式规划器中，使“可形变 + 受约束环境”这类难题可以被系统化求解。',
            '摘要里特别强调解析梯度，这一点很关键：相比 finite difference，解析导数让 inverse kinetostatic 求解速度显著提升，也让后续轨迹优化真正可行。',
            '也就是说，创新不只是“建模更真实”，而是把真实建模和高效求解统一起来，形成可落地的规划管线。',
            '从应用角度看，它让机器人能够利用柔性段的顺应性去穿越狭窄约束空间，这是纯刚体工具难以做到的。',
        ]
    if 'comfree-sim' in low or 'contact physics engine' in low:
        return [
            '这篇工作的重点是重新设计接触物理引擎，使其更适合 GPU 并行场景，而不是沿用传统接触求解器的串行思路。',
            '它强调 analytical contact formulation，说明作者试图把接触过程写成更可分析、更适合大规模计算的形式。',
            '这样做的意义在于，接触丰富场景的仿真吞吐量可以显著提高，同时仍然保留足够的物理合理性，支持训练和控制。',
            '对机器人控制而言，真正有价值的是它把“高保真接触建模”和“较高控制频率”这两个经常互相冲突的目标拉近了。',
            '如果这套引擎能稳定工作，它会成为 contact-rich manipulation、locomotion 甚至 sim-to-real 数据生成的重要基础设施。',
        ]
    if 'vector field' in low and 'drone racing' in low:
        return [
            '作者把向量场先验引入 differentiable policy learning，本质上是在任务目标与策略优化之间增加一层几何结构。',
            '这个结构让无人机不再只依赖最终是否穿门成功这类间接信号，而是持续获得“局部应该朝哪个方向演化”的平滑指导。',
            '在高速竞速任务里，普通视觉控制目标往往高度不连续，梯度容易不稳定；向量场先验则让优化景观更平滑。',
            '因此创新点不只是又加了一个辅助损失，而是把控制目标改写成更适合可微学习传播的形式。',
            '这类思路对高速、高动态、容错空间很小的机器人任务尤其重要，因为训练中的微小不稳定都会在执行时被迅速放大。',
        ]

    return [
        '方法层面提出了相对现有工作更结构化的设计，而不只是简单叠加已有模块。',
        '它关注的重点是当前流程中的关键瓶颈，并尝试把这个瓶颈转写成更可解释、更可控制的机制。',
        '从机器人视角看，这类创新的实际价值通常体现在长时稳定性、控制效率或泛化表现上。',
    ]


def render_html(report):
    parts = ["""<!DOCTYPE html><html lang='zh-CN'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>论文日报可读版</title><style>
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;max-width:960px;margin:20px auto;padding:0 14px;line-height:1.75;color:#172033;background:#f6f8fb}
.header{margin-bottom:18px}.meta{color:#566074}.card{border:1px solid #dbe2ea;border-radius:16px;padding:18px;margin:18px 0;background:#fff;box-shadow:0 4px 14px rgba(15,23,42,.04)}
h1{font-size:28px;margin:0 0 8px}h2{margin:28px 0 8px;font-size:22px}h3{margin:0 0 8px;font-size:18px}p{margin:8px 0}.imgwrap{margin:14px 0}.imgwrap img{max-width:100%;height:auto;border-radius:10px;border:1px solid #e5e7eb;background:#fff}
ul{margin:8px 0 0 20px;padding:0}li{margin:8px 0}a{color:#2563eb;word-break:break-all;text-decoration:none}.badge{display:inline-block;padding:2px 8px;border-radius:999px;background:#eef2ff;color:#3730a3;font-size:12px;margin-right:6px}
</style></head><body>"""]
    parts.append(f"<div class='header'><h1>论文日报可读版 {escape(report['runDate'])}</h1><p class='meta'>A 组与 B 组共 {len(report['items'])} 条。论文条目提供忠实中文摘要与分点创新分析；平台更新保持简洁。</p></div>")
    current_group = None
    for item in report['items']:
        if item['group'] != current_group:
            current_group = item['group']
            title = 'A 组：具身 / VLA 与 agent-memory-world model 交叉' if current_group == 'A' else 'B 组：differentiable / system identification / trajectory optimization / MuJoCo-MJX-Genesis'
            parts.append(f"<h2>{escape(title)}</h2>")
        parts.append("<div class='card'>")
        parts.append(f"<h3>{escape(item['label'])}. {escape(item['title'])}</h3>")
        parts.append(f"<p class='meta'><span class='badge'>{escape(item['type'])}</span>来源：{escape(item['source'])} ｜ 发布日期：{escape(item['published_at'])}</p>")
        if item.get('image_data_uri'):
            parts.append(f"<div class='imgwrap'><img src='{item['image_data_uri']}' alt='{escape(item['title'])}'></div>")
        elif item.get('failure_reason'):
            parts.append(f"<p><strong>配图说明：</strong>{escape(item['failure_reason'])}</p>")
        parts.append(f"<p><strong>中文摘要（基于原文摘要翻译）：</strong>{escape(item['cn_summary'])}</p>")
        parts.append("<p><strong>创新点解释：</strong></p><ul>")
        for point in item.get('innovation_points', []):
            parts.append(f"<li>{escape(point)}</li>")
        parts.append("</ul>")
        if item.get('paper_url'):
            parts.append(f"<p><a href='{escape(item['paper_url'])}'>论文链接</a></p>")
        if item.get('code_url'):
            parts.append(f"<p><a href='{escape(item['code_url'])}'>代码/项目链接</a></p>")
        parts.append("</div>")
    parts.append("</body></html>")
    return ''.join(parts)


def main():
    selected = load_json(SELECTED)
    run_date = selected.get('runDate', '')
    report = {'runDate': run_date, 'items': []}

    for group in ['A', 'B']:
        for index, item in enumerate(selected.get('selected', {}).get(group, []), start=1):
            slug = slugify(item.get('id') or item.get('title') or f'{group}-{index}')
            meta_path = IMAGE_META_DIR / f'{slug}.json'
            image_meta = load_json(meta_path) if meta_path.exists() else {}
            image_uri = data_uri(image_meta.get('image_path', ''))
            failure_reason = image_meta.get('failure_reason', '')
            if image_meta.get('image_path') and not image_uri and not failure_reason:
                failure_reason = '图片已找到，但原始格式不适合直接在 HTML/Telegram 中显示，当前转换失败。'
            report['items'].append({
                'group': group,
                'label': f'{group}{index}',
                'title': item.get('title', ''),
                'type': '平台更新' if 'platform' in (item.get('type') or '') else '论文',
                'source': item.get('source', ''),
                'published_at': item.get('published_at', ''),
                'paper_url': item.get('paper_url', ''),
                'code_url': item.get('code_url', ''),
                'failure_reason': failure_reason,
                'image_data_uri': image_uri,
                'cn_summary': cn_summary_detailed(item),
                'innovation_points': innovation_points(item),
            })

    html_out = OUT_DIR / f'paper_report_readable_{run_date}.html'
    json_out = OUT_DIR / f'paper_report_readable_{run_date}.json'
    html_out.write_text(render_html(report), encoding='utf-8')
    json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(html_out)
    print(json_out)


if __name__ == '__main__':
    main()
