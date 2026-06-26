import { useState } from "react";
import API_CONFIG from "./config";

const SYSTEM_PROMPT = `你是一位专业的 AI 图像提示词工程师，精通将模糊的创意想法转化为结构严谨、可执行的图像生成规格书。

你的提示词生成方法论基于"五层拆解法"，并遵循以下核心原则：

【核心原则】
1. 画面先行：先用自然语言描述整体画面，让人一眼理解要画什么
2. 五层拆解：整体基调 → 质感材质 → 笔触细节 → 构图规则 → 文字系统（按需）
3. 正向为主：每层重点描述"要什么"，仅在AI容易犯错的关键点标注"避免"
4. 抽象词翻译：将模糊审美词转化为具体可感知的视觉现象
5. 参照物锚定：用风格/元素/反向参照锁定模糊地带

【智能判断规则】
- "文字系统"模块仅在画面需要文字元素时输出（如信息图、海报、卡片）。纯插画/风景/人像等场景直接跳过此模块。
- "避免"条目仅在该层确实存在AI容易误判的情况下才写，不要每层都机械地加排除项。

【输出格式要求】
严格按照以下结构输出，使用中文，每个模块用标题分隔，内容精炼但具体：

---
# 🎨 图片提示词

## 画面介绍
[用2-3句自然语言描述画面：主题是什么、场景在哪里、画面主体是谁/什么、在做什么、整体感觉如何]

## 整体基调
- 风格：[具体风格名称]
- 氛围：[2-3个情绪词]

## 质感材质
- 介质感：[具体描述，如介质/工艺/肌理]

## 笔触细节
- 线条：[具体线条特征]
- 色彩：[主色调、辅助色、点缀色及其分布逻辑]

## 构图规则
- 版式：[比例，如竖版3:4]
- 布局：[元素分布逻辑、视觉动线]

## 文字系统（仅在画面包含文字时输出）
- 字体感：[字体风格描述]
- 层级：[标题/正文的视觉差异]

## 参照物
- 风格参照：[1-2个具体参照，附简要说明为什么参照]
- 反向排除：[不想要的风格]

---

## 💡 可执行提示词

根据用户选择的目标工具，输出对应格式的提示词：

**通用中文提示词：**
[将规格书浓缩为一段完整的中文描述，包含主体、场景、风格、质感、色彩、构图等核心要素，适用于国产AI绘图工具（如通义万相、文心一格、LiblibAI等），2-4句话]

**Midjourney：**
[完整英文提示词，按"主体描述, 环境/场景, 风格/质感, 色彩/光影, 氛围/情绪"顺序组织关键词，末尾附带参数如 --ar 3:4 --s 500 --v 6.1 等]

**DALL-E：**
[纯自然语言英文描述，不使用任何参数标记，将风格和细节融入句子中，1-3句话]

**Stable Diffusion：**
prompt: [英文正向提示词，逗号分隔的关键词]
negative prompt: [英文反向提示词，逗号分隔]

---

【风格预设知识库】
当用户使用以下风格预设时，严格遵循对应的视觉规范：

🖍️ 童趣涂鸦：
- 质感：蜡笔/彩色铅笔在粗糙画纸上的手绘感，笔触不均匀，有涂出边界的随意感
- 线条：粗拙歪扭的轮廓线，不追求精准，像6-8岁儿童画的
- 色彩：高饱和的红黄蓝绿基础色，色块填充不均匀，偶尔留白
- 构图：元素随意散布，无严格透视，大小比例夸张
- 参照：Crayon Shin-chan 背景画风、儿童绘本插画

📐 极简现代：
- 质感：哑光纸面或屏幕渲染的干净平面，无任何纹理噪点
- 线条：几何化的精确线条，或完全无线条只用色块
- 色彩：大面积留白+1-2种主题色，色彩克制，明度对比为主
- 构图：大量负空间，元素居中或严格网格对齐，呼吸感强
- 参照：无印良品广告、Dieter Rams 设计语言

🎞️ 复古胶片：
- 质感：胶片颗粒感明显，边缘轻微暗角，偶尔有光晕漏光
- 线条：无明显线稿，以光影和色块塑形
- 色彩：偏黄绿的暗部，褪色的高光，整体色温偏暖，饱和度降低，类似Kodak Gold 200
- 构图：随意抓拍感，主体不一定居中，有生活化的构图
- 参照：1970s-80s 柯达胶卷照片、滨田英明摄影

🌸 日系插画：
- 质感：数字扁平插画的干净感，或淡彩水彩的透明感
- 线条：纤细均匀的描边线，圆润柔和
- 色彩：低饱和粉彩色系（薄荷绿、樱花粉、天空蓝、奶油黄），明度高
- 构图：留白舒适，元素简洁不堆砌，视觉重心偏下
- 参照：Loundraw、米山舞的插画风格、《你的名字》色调

⚙️ 赛博朋克：
- 质感：光滑金属与潮湿街道的反射，霓虹灯在雨水中的漫反射
- 线条：锐利的几何切割，硬边轮廓
- 色彩：深黑/深蓝底色上的霓虹品红、电光蓝、酸性绿，强烈冷暖对比
- 构图：仰视或极端透视，密集的视觉信息，纵深感强
- 参照：《银翼杀手2049》、Beeple 数字艺术

📚 学术信息图：
- 质感：印刷级的清晰锐利，干净的白色或浅灰底
- 线条：规范的图标线条，统一粗细，圆角处理
- 色彩：3-4色系统配色方案，一个主色+中性辅色，用色块区分信息层级
- 构图：严格的网格系统，信息从上到下或从左到右流动，箭头/连线引导阅读顺序
- 参照：《经济学人》信息图、Behance 上的数据可视化作品
- 文字系统必须输出：标题用无衬线粗体，正文清晰易读，数据用大号突出

【关键要求】
- 可执行提示词是最终产出物，必须保证从中文规格书到英文提示词的信息完整传递，不能只是简单概括
- 英文提示词中的视觉关键词应精准对应规格书中的具体描述，不要泛化
- 如果用户输入很简单，要主动补全合理的细节
- 当用户选择了风格预设，五层拆解的每一层必须体现该预设的视觉规范，不能只是泛泛描述`;

const TOOL_OPTIONS = [
  { label: "全部", value: "all" },
  { label: "Midjourney", value: "midjourney" },
  { label: "DALL-E", value: "dalle" },
  { label: "Stable Diffusion", value: "sd" },
];

const STYLE_PRESETS = [
  { label: "🖍️ 童趣涂鸦", value: "儿童手绘涂鸦风格，彩色铅笔质感，活泼热闹" },
  { label: "📐 极简现代", value: "极简主义，现代设计感，大量留白，几何构图" },
  { label: "🎞️ 复古胶片", value: "复古胶片风格，1970s色调，颗粒感，老照片质感" },
  { label: "🌸 日系插画", value: "日系小清新插画，柔和色彩，扁平风，治愈系" },
  { label: "⚙️ 赛博朋克", value: "赛博朋克风格，霓虹色彩，科技感，暗黑背景" },
  { label: "📚 学术信息图", value: "专业信息图，学术风格，数据可视化，清晰易读" },
];

export default function App() {
  const [input, setInput] = useState("");
  const [selectedPreset, setSelectedPreset] = useState("");
  const [selectedTool, setSelectedTool] = useState("all");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const handlePreset = (val) => {
    setSelectedPreset(val);
    setInput(val);
  };

  const generate = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setResult("");
    try {
      const res = await fetch(API_CONFIG.baseURL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          model: API_CONFIG.model,
          max_tokens: API_CONFIG.maxTokens,
          messages: [
            { role: "system", content: SYSTEM_PROMPT },
            { role: "user", content: `请为以下需求生成专业的图片提示词：\n\n${input}\n\n目标工具：${selectedTool === "all" ? "请同时输出 Midjourney、DALL-E、Stable Diffusion 三种格式" : selectedTool === "midjourney" ? "仅输出 Midjourney 格式" : selectedTool === "dalle" ? "仅输出 DALL-E 格式" : "仅输出 Stable Diffusion 格式（含 negative prompt）"}` },
          ],
        }),
      });
      const data = await res.json();
      const text = data.choices?.[0]?.message?.content || "生成失败，请重试。";
      setResult(text);
    } catch (e) {
      setResult("⚠️ 请求失败，请检查网络后重试。");
    }
    setLoading(false);
  };

  const copyResult = () => {
    navigator.clipboard.writeText(result);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const renderMarkdown = (text) => {
    const lines = text.split("\n");
    return lines.map((line, i) => {
      if (line.startsWith("# ")) return <h1 key={i} style={{fontSize:"1.3rem",fontWeight:700,margin:"1rem 0 0.5rem",color:"#1a1a2e"}}>{line.slice(2)}</h1>;
      if (line.startsWith("## ")) return <h2 key={i} style={{fontSize:"1rem",fontWeight:700,margin:"0.8rem 0 0.3rem",color:"#4a4e69",borderBottom:"1px solid #e8e8f0",paddingBottom:"0.2rem"}}>{line.slice(3)}</h2>;
      if (line.startsWith("- ")) return <div key={i} style={{display:"flex",gap:"0.4rem",marginBottom:"0.2rem",lineHeight:1.6}}><span style={{color:"#9b5de5",flexShrink:0}}>•</span><span style={{color:"#333",fontSize:"0.88rem"}}>{renderInline(line.slice(2))}</span></div>;
      if (line.startsWith("---")) return <hr key={i} style={{border:"none",borderTop:"1px dashed #ddd",margin:"0.6rem 0"}}/>;
      if (line.trim() === "") return <div key={i} style={{height:"0.3rem"}}/>;
      return <p key={i} style={{color:"#333",fontSize:"0.88rem",lineHeight:1.7,margin:"0.1rem 0"}}>{renderInline(line)}</p>;
    });
  };

  const renderInline = (text) => {
    const parts = text.split(/(\*\*[^*]+\*\*|\`[^`]+\`)/g);
    return parts.map((p, i) => {
      if (p.startsWith("**") && p.endsWith("**")) return <strong key={i} style={{color:"#1a1a2e"}}>{p.slice(2,-2)}</strong>;
      if (p.startsWith("`") && p.endsWith("`")) return <code key={i} style={{background:"#f0eeff",color:"#7c3aed",padding:"0 4px",borderRadius:3,fontSize:"0.85rem"}}>{p.slice(1,-1)}</code>;
      return p;
    });
  };

  return (
    <div style={{minHeight:"100vh",background:"linear-gradient(135deg,#f0eeff 0%,#fef9ff 50%,#eff6ff 100%)",fontFamily:"'PingFang SC','Microsoft YaHei',sans-serif",padding:"1.5rem 1rem"}}>
      <div style={{maxWidth:720,margin:"0 auto"}}>

        {/* Header */}
        <div style={{textAlign:"center",marginBottom:"1.5rem"}}>
          <div style={{fontSize:"2.5rem",marginBottom:"0.4rem"}}>✏️</div>
          <h1 style={{fontSize:"1.5rem",fontWeight:800,color:"#1a1a2e",margin:0}}>图片提示词生成器</h1>
          <p style={{color:"#6b7280",fontSize:"0.88rem",marginTop:"0.4rem"}}>基于五层拆解法，将创意想法转化为专业的 AI 图像生成规格书</p>
        </div>

        {/* Presets */}
        <div style={{marginBottom:"1rem"}}>
          <div style={{fontSize:"0.8rem",color:"#9b5de5",fontWeight:600,marginBottom:"0.5rem",letterSpacing:"0.05em"}}>快速风格预设</div>
          <div style={{display:"flex",flexWrap:"wrap",gap:"0.4rem"}}>
            {STYLE_PRESETS.map(p => (
              <button key={p.value} onClick={() => handlePreset(p.value)}
                style={{padding:"0.3rem 0.7rem",borderRadius:20,border:`1.5px solid ${selectedPreset===p.value?"#9b5de5":"#e0d9f7"}`,background:selectedPreset===p.value?"#9b5de5":"white",color:selectedPreset===p.value?"white":"#4a4e69",fontSize:"0.8rem",cursor:"pointer",transition:"all 0.2s"}}>
                {p.label}
              </button>
            ))}
          </div>
        </div>

        {/* Tool selector */}
        <div style={{marginBottom:"1rem"}}>
          <div style={{fontSize:"0.8rem",color:"#9b5de5",fontWeight:600,marginBottom:"0.5rem",letterSpacing:"0.05em"}}>目标生成工具</div>
          <div style={{display:"flex",flexWrap:"wrap",gap:"0.4rem"}}>
            {TOOL_OPTIONS.map(t => (
              <button key={t.value} onClick={() => setSelectedTool(t.value)}
                style={{padding:"0.3rem 0.7rem",borderRadius:20,border:`1.5px solid ${selectedTool===t.value?"#6b48c8":"#e0d9f7"}`,background:selectedTool===t.value?"#6b48c8":"white",color:selectedTool===t.value?"white":"#4a4e69",fontSize:"0.8rem",cursor:"pointer",transition:"all 0.2s"}}>
                {t.label}
              </button>
            ))}
          </div>
        </div>

        {/* Input */}
        <div style={{background:"white",borderRadius:16,border:"1.5px solid #e0d9f7",overflow:"hidden",boxShadow:"0 2px 12px rgba(155,93,229,0.08)",marginBottom:"1rem"}}>
          <textarea
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="描述你想要的图片内容或风格...&#10;例如：一张介绍「深度学习原理」的信息图，面向初学者，风格轻松有趣"
            style={{width:"100%",minHeight:110,padding:"1rem",border:"none",outline:"none",fontSize:"0.9rem",lineHeight:1.7,color:"#1a1a2e",resize:"vertical",boxSizing:"border-box",fontFamily:"inherit"}}
          />
          <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",padding:"0.6rem 1rem",borderTop:"1px solid #f3f0ff",background:"#faf9ff"}}>
            <span style={{fontSize:"0.75rem",color:"#aaa"}}>{input.length} 字</span>
            <button onClick={generate} disabled={loading || !input.trim()}
              style={{padding:"0.45rem 1.4rem",borderRadius:20,border:"none",background:loading||!input.trim()?"#e0d9f7":"linear-gradient(135deg,#9b5de5,#6b48c8)",color:loading||!input.trim()?"#aaa":"white",fontWeight:700,fontSize:"0.88rem",cursor:loading||!input.trim()?"not-allowed":"pointer",transition:"all 0.2s",boxShadow:loading||!input.trim()?"none":"0 2px 8px rgba(155,93,229,0.3)"}}>
              {loading ? "⏳ 生成中..." : "✨ 生成提示词"}
            </button>
          </div>
        </div>

        {/* Loading */}
        {loading && (
          <div style={{textAlign:"center",padding:"2rem",color:"#9b5de5"}}>
            <div style={{fontSize:"2rem",animation:"spin 1s linear infinite",display:"inline-block"}}>⚙️</div>
            <p style={{marginTop:"0.5rem",fontSize:"0.85rem",color:"#6b7280"}}>正在分析需求，构建五层规格书...</p>
          </div>
        )}

        {/* Result */}
        {result && !loading && (
          <div style={{background:"white",borderRadius:16,border:"1.5px solid #e0d9f7",boxShadow:"0 2px 16px rgba(155,93,229,0.1)",overflow:"hidden"}}>
            <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",padding:"0.7rem 1rem",borderBottom:"1px solid #f3f0ff",background:"linear-gradient(90deg,#faf9ff,#f5f3ff)"}}>
              <span style={{fontWeight:700,color:"#4a4e69",fontSize:"0.88rem"}}>📋 生成结果</span>
              <button onClick={copyResult}
                style={{padding:"0.3rem 0.9rem",borderRadius:20,border:"1.5px solid #e0d9f7",background:copied?"#9b5de5":"white",color:copied?"white":"#9b5de5",fontSize:"0.78rem",cursor:"pointer",fontWeight:600,transition:"all 0.2s"}}>
                {copied ? "✅ 已复制" : "📄 复制全文"}
              </button>
            </div>
            <div style={{padding:"1rem 1.2rem",maxHeight:500,overflowY:"auto"}}>
              {renderMarkdown(result)}
            </div>
          </div>
        )}

        {/* Method hint */}
        <div style={{marginTop:"1.2rem",padding:"0.8rem 1rem",background:"rgba(155,93,229,0.05)",borderRadius:12,border:"1px dashed #d4c6f7"}}>
          <div style={{fontSize:"0.75rem",color:"#7c5cbf",fontWeight:600,marginBottom:"0.3rem"}}>💡 五层拆解法</div>
          <div style={{display:"flex",gap:"0.4rem",flexWrap:"wrap"}}>
            {["画面介绍","整体基调","质感材质","笔触细节","构图规则"].map((s,i)=>(
              <span key={i} style={{fontSize:"0.72rem",background:"white",color:"#9b5de5",padding:"0.15rem 0.6rem",borderRadius:10,border:"1px solid #e0d9f7"}}>
                {i+1}. {s}
              </span>
            ))}
          </div>
        </div>

      </div>

      <style>{`@keyframes spin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}`}</style>
    </div>
  );
}