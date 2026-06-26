const el = (tag, attrs = {}, ...children) => {
  const node = document.createElement(tag);
  Object.entries(attrs).forEach(([key, value]) => {
    if (value == null) return;
    if (key === "class") node.className = value;
    else if (key === "html") node.innerHTML = value;
    else node.setAttribute(key, value);
  });
  children.flat().forEach(child => {
    if (child == null) return;
    node.append(child.nodeType ? child : document.createTextNode(String(child)));
  });
  return node;
};

const esc = value => String(value ?? "").replace(/[&<>"']/g, ch => ({
  "&": "&amp;",
  "<": "&lt;",
  ">": "&gt;",
  '"': "&quot;",
  "'": "&#039;"
}[ch]));

async function fetchText(path) {
  const response = await fetch(`../${path}`, { cache: "no-store" });
  if (!response.ok) return "";
  return response.text();
}

async function loadBundle() {
  const response = await fetch("../analysis_bundle.json", { cache: "no-store" });
  if (!response.ok) throw new Error(`无法加载 analysis_bundle.json：${response.status}`);
  return response.json();
}

function inlineMarkdown(text) {
  return esc(text)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
}

function markdownToHtml(markdown) {
  const lines = markdown.replace(/\r\n/g, "\n").split("\n");
  const out = [];
  let inCode = false;
  let codeLang = "";
  let code = [];
  let para = [];
  let list = [];
  let table = [];

  const flushPara = () => {
    if (!para.length) return;
    out.push(`<p>${inlineMarkdown(para.join(" "))}</p>`);
    para = [];
  };
  const flushList = () => {
    if (!list.length) return;
    out.push(`<ul>${list.map(item => `<li>${inlineMarkdown(item)}</li>`).join("")}</ul>`);
    list = [];
  };
  const flushTable = () => {
    if (!table.length) return;
    const sep = /^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/;
    const rows = table.filter(row => !sep.test(row));
    if (rows.length) {
      const htmlRows = rows.map((row, idx) => {
        const cells = row.trim().replace(/^\|/, "").replace(/\|$/, "").split("|")
          .map(cell => inlineMarkdown(cell.trim()));
        const tag = idx === 0 ? "th" : "td";
        return `<tr>${cells.map(cell => `<${tag}>${cell}</${tag}>`).join("")}</tr>`;
      }).join("");
      out.push(`<table>${htmlRows}</table>`);
    }
    table = [];
  };
  const flushAll = () => {
    flushPara();
    flushList();
    flushTable();
  };
  const pushCode = raw => {
    if (["math", "latex", "tex"].includes(codeLang)) {
      out.push(`<div class="formula"><div class="math markdown-math" data-math="${esc(raw)}"></div><div class="fallback">${esc(raw)}</div></div>`);
    } else {
      out.push(`<pre>${esc(raw)}</pre>`);
    }
  };

  for (const line of lines) {
    if (line.startsWith("```")) {
      if (inCode) {
        pushCode(code.join("\n"));
        code = [];
        inCode = false;
        codeLang = "";
      } else {
        flushAll();
        inCode = true;
        codeLang = line.replace(/^```/, "").trim().toLowerCase();
      }
      continue;
    }
    if (inCode) {
      code.push(line);
      continue;
    }
    if (!line.trim()) {
      flushAll();
      continue;
    }
    if (line.trim().startsWith("|") && line.includes("|")) {
      flushPara();
      flushList();
      table.push(line);
      continue;
    }
    if (/^#{1,4}\s+/.test(line)) {
      flushAll();
      const level = Math.min((line.match(/^#+/) || [""])[0].length + 1, 4);
      out.push(`<h${level}>${inlineMarkdown(line.replace(/^#+\s+/, ""))}</h${level}>`);
      continue;
    }
    if (/^\s*[-*]\s+/.test(line)) {
      flushPara();
      flushTable();
      list.push(line.replace(/^\s*[-*]\s+/, ""));
      continue;
    }
    if (/^\s*\d+\.\s+/.test(line)) {
      flushPara();
      flushTable();
      list.push(line.replace(/^\s*\d+\.\s+/, ""));
      continue;
    }
    para.push(line.trim());
  }
  flushAll();
  if (inCode && code.length) pushCode(code.join("\n"));
  return out.join("\n");
}

function formulaSource(formula) {
  return formula?.math || formula?.latex || formula?.tex || "";
}

function renderFormula(formula) {
  const source = formulaSource(formula);
  const box = el("div", { class: "formula" });
  const math = el("div", { class: "math" });
  const fallback = el("div", { class: "fallback" }, formula?.fallback || source);
  box.append(math, fallback);
  if (window.katex && source) {
    try {
      katex.render(source, math, { throwOnError: false, displayMode: true });
      box.classList.add("formula-rendered");
    } catch {
      math.textContent = formula?.fallback || source;
      box.classList.add("formula-failed");
    }
  } else {
    math.textContent = formula?.fallback || source || "未提供公式";
    box.classList.add("formula-failed");
  }
  return box;
}

function renderMarkdownMath(root) {
  root.querySelectorAll(".markdown-math[data-math]").forEach(node => {
    const source = node.getAttribute("data-math") || "";
    const box = node.closest(".formula");
    if (window.katex && source) {
      try {
        katex.render(source, node, { throwOnError: false, displayMode: true });
        box?.classList.add("formula-rendered");
        box?.classList.remove("formula-failed");
      } catch {
        node.textContent = source;
        box?.classList.add("formula-failed");
      }
    } else {
      node.textContent = source;
      box?.classList.add("formula-failed");
    }
  });
}

function asArray(value) {
  return Array.isArray(value) ? value : [];
}

function renderSummary(bundle) {
  const section = document.getElementById("summary");
  const checks = asArray(bundle.validation?.checks)
    .map(c => `<span class="pill">${esc(c.name)}：${esc(c.status)}</span>`)
    .join("");
  section.innerHTML = `
    <h2>总览</h2>
    <p class="note">${esc(bundle.domain_critical_execution?.description || "该分析把论文方法、源码实现、实验入口和验证状态放在同一套证据链中。")}</p>
    <div class="meta">
      <span class="pill">PDF ${esc(bundle.intake?.paper?.page_count ?? "unknown")} 页</span>
      <span class="pill">${esc(bundle.schema_version || "unknown schema")}</span>
      <span class="pill">commit ${esc(bundle.intake?.repository?.commit ?? "unknown")}</span>
      <span class="pill">${esc(bundle.validation?.final_status || "未记录最终状态")}</span>
    </div>
    <h3>分析范围</h3>
    <p>${esc(bundle.intake?.scope || "未记录分析范围。")}</p>
    <h3>验证状态</h3>
    <div class="meta">${checks || "<span class='pill'>未记录检查项</span>"}</div>
  `;
}

async function renderReport() {
  const section = document.getElementById("report");
  const report = await fetchText("paper_reading_report.md");
  if (!report.trim()) {
    section.innerHTML = "<h2>论文解读报告</h2><p class='empty'>未找到 paper_reading_report.md。</p>";
    return;
  }
  section.innerHTML = `<h2>论文解读报告</h2><div class="markdown searchable">${markdownToHtml(report)}</div>`;
  renderMarkdownMath(section);
}

async function renderQuestions(bundle) {
  const section = document.getElementById("questions");
  const markdown = await fetchText("paper_questions_for_code.md");
  const questions = asArray(bundle.paper_questions);
  const rows = questions.map(item => `
    <tr class="searchable">
      <td><strong>${esc(item.id)}</strong><br>${esc(item.question)}</td>
      <td>${esc(item.why_it_matters)}</td>
      <td>${asArray(item.paper_evidence).map(e => `<div>${esc(e)}</div>`).join("") || "未记录"}</td>
      <td>${asArray(item.code_evidence).map(e => `<code>${esc(e)}</code>`).join("<br>") || "未记录"}</td>
      <td>${esc(item.status)}<br>${esc(item.answer)}</td>
    </tr>`).join("");
  section.innerHTML = `
    <h2>阅读疑问</h2>
    <p>这一节先列出 PDF 中没有说清楚、公式或模型含糊、实验落地缺少细节、前后可能不一致的问题，再说明代码如何回答或仍然无法回答。</p>
    ${markdown.trim() ? `<div class="markdown searchable">${markdownToHtml(markdown)}</div>` : ""}
    <table><thead><tr><th>问题</th><th>为什么重要</th><th>论文证据</th><th>代码证据</th><th>结论</th></tr></thead><tbody>${rows || "<tr><td colspan='5'>未记录阅读疑问。</td></tr>"}</tbody></table>
  `;
  renderMarkdownMath(section);
}

function renderMechanisms(bundle) {
  const section = document.getElementById("mechanisms");
  section.innerHTML = "<h2>理论到代码</h2><p>每个机制按论文公式/步骤、代码入口、关键片段、实现关系和差异组织。公式必须是可渲染数学式，解释另列。</p>";
  asArray(bundle.mechanisms).forEach(mech => {
    const block = el("article", { class: "block searchable" });
    block.append(el("h3", {}, mech.name || "未命名机制"));
    block.append(el("p", {}, mech.paper_claim || "未记录论文主张。"));
    if (asArray(mech.formulas).length) {
      block.append(el("div", { class: "formula-list" }, asArray(mech.formulas).map(renderFormula)));
    }
    const rows = asArray(mech.code_indices).map(idx => `
      <tr>
        <td><code>${esc(idx.path)}${idx.line_range ? ":" + esc(idx.line_range) : ""}</code></td>
        <td>${asArray(idx.symbols).map(s => `<code>${esc(s)}</code>`).join(", ")}</td>
        <td>${esc(idx.role)}</td>
      </tr>`).join("");
    block.append(el("table", { html: `<thead><tr><th>代码索引</th><th>符号/方法</th><th>作用</th></tr></thead><tbody>${rows || "<tr><td colspan='3'>未记录代码索引</td></tr>"}</tbody>` }));
    block.append(el("p", {}, `实现关系：${mech.relationship || "未记录。"}`));
    if (asArray(mech.differences).length) {
      block.append(el("h4", {}, "论文与代码差异"));
      block.append(el("ul", {}, asArray(mech.differences).map(d => el("li", {}, d))));
    }
    section.append(block);
  });
}

function renderExperiments(bundle) {
  const rows = asArray(bundle.experiments).map(exp => `
    <tr class="searchable">
      <td><strong>${esc(exp.paper_ref)}</strong><br>${esc(exp.intent)}</td>
      <td><pre>${esc(JSON.stringify(exp.settings || {}, null, 2))}</pre></td>
      <td>${asArray(exp.code_paths).map(p => `<code>${esc(p)}</code>`).join("<br>")}</td>
      <td><span class="status-${esc(exp.command_status)}">${esc(exp.command_status)}</span><br>${asArray(exp.commands).map(c => `<code>${esc(c)}</code>`).join("<br>")}</td>
      <td>${esc(exp.result_extraction)}<ul>${asArray(exp.code_disclosed_omissions).map(o => `<li>${esc(o)}</li>`).join("")}</ul></td>
    </tr>`).join("");
  document.getElementById("experiments").innerHTML = `
    <h2>实验理解</h2>
    <p>每个论文表格、图、消融或补充实验都要对应代码路径、命令状态、结果提取方式和代码揭示的缺口。</p>
    <table><thead><tr><th>论文实验</th><th>设置</th><th>代码路径</th><th>命令状态</th><th>结果与缺口</th></tr></thead><tbody>${rows || "<tr><td colspan='5'>未记录实验映射。</td></tr>"}</tbody></table>
  `;
}

function renderOmissions(bundle) {
  const rows = asArray(bundle.implementation_omissions).map(item => `
    <tr class="searchable">
      <td><strong>${esc(item.detail)}</strong></td>
      <td>${esc(item.paper_says)}</td>
      <td>${esc(item.code_does)}</td>
      <td>${esc(item.impact)}<br>${asArray(item.evidence).map(e => `<code>${esc(e)}</code>`).join("<br>")}</td>
    </tr>`).join("");
  document.getElementById("omissions").innerHTML = `
    <h2>论文未披露但代码说明的细节</h2>
    <table><thead><tr><th>细节</th><th>论文说法</th><th>代码事实</th><th>影响</th></tr></thead><tbody>${rows || "<tr><td colspan='4'>未记录未披露细节。</td></tr>"}</tbody></table>
  `;
}

function extractMermaidBlocks(markdown) {
  const blocks = [];
  const re = /```mermaid\s*([\s\S]*?)```/g;
  let match;
  while ((match = re.exec(markdown))) blocks.push(match[1].trim());
  return blocks;
}

async function renderDiagrams(bundle) {
  const section = document.getElementById("diagrams");
  section.innerHTML = "<h2>UML 与流程</h2><p>图表由 Mermaid 源码渲染。渲染失败时显示源码，不出现空白。</p>";
  const diagramMd = await fetchText("diagrams.md");
  const mermaidBlocks = extractMermaidBlocks(diagramMd);
  const labels = asArray(bundle.diagrams).map((d, i) => d.title || `图 ${i + 1}`);
  const tabs = el("div", { class: "diagram-tabs" });
  const box = el("div", { class: "diagram-box" });
  const legend = el("p", { class: "note" });
  const source = el("details", {}, el("summary", {}, "查看 Mermaid 源码"), el("pre", {}));
  section.append(tabs, legend, box, source);

  async function show(index) {
    [...tabs.children].forEach((btn, i) => btn.classList.toggle("active", i === index));
    const text = mermaidBlocks[index] || "";
    const diagram = asArray(bundle.diagrams)[index] || {};
    legend.textContent = diagram.legend || "未记录图例。";
    source.querySelector("pre").textContent = text || "未在 diagrams.md 中找到 Mermaid 源码。";
    if (!text) {
      box.innerHTML = "<p class='empty'>未找到 Mermaid 源码。</p>";
      return;
    }
    if (!window.mermaid) {
      box.innerHTML = `<p class="note">Mermaid 脚本未加载，当前显示源码。</p><pre>${esc(text)}</pre>`;
      return;
    }
    try {
      const { svg } = await mermaid.render(`diagram-${Date.now()}-${index}`, text);
      box.innerHTML = svg;
    } catch (err) {
      box.innerHTML = `<p class="note">Mermaid 渲染失败，当前显示源码。${esc(err.message || "")}</p><pre>${esc(text)}</pre>`;
    }
  }

  if (window.mermaid) {
    mermaid.initialize({ startOnLoad: false, securityLevel: "strict", theme: "base" });
  }
  const count = Math.max(labels.length, mermaidBlocks.length);
  for (let i = 0; i < count; i++) {
    const btn = el("button", { type: "button" }, labels[i] || `图 ${i + 1}`);
    btn.addEventListener("click", () => show(i));
    tabs.append(btn);
  }
  if (count) setTimeout(() => show(0), 0);
  else box.innerHTML = "<p class='empty'>没有图表条目。</p>";
}

function renderModify(bundle) {
  const rows = asArray(bundle.modify_guide).map(item => `
    <tr class="searchable">
      <td><strong>${esc(item.goal)}</strong></td>
      <td>${asArray(item.files_methods).map(m => `<code>${esc(m)}</code>`).join("<br>")}</td>
      <td>${esc(item.minimal_change)}</td>
      <td><ul>${asArray(item.invariants).map(i => `<li>${esc(i)}</li>`).join("")}</ul></td>
      <td>${esc(item.smoke_test)}</td>
    </tr>`).join("");
  document.getElementById("modify").innerHTML = `
    <h2>改方法指南</h2>
    <p>这里指修改论文提出的方法层，而不是泛泛替换 backbone。架构替换、实验设置修改和方法组件修改应分开说明。</p>
    <table><thead><tr><th>目标</th><th>文件/方法</th><th>最小改动</th><th>必须保持</th><th>烟测</th></tr></thead><tbody>${rows || "<tr><td colspan='5'>未记录修改指南。</td></tr>"}</tbody></table>
  `;
}

function renderValidation(bundle) {
  const rows = asArray(bundle.validation?.checks).map(c => `<tr><td>${esc(c.name)}</td><td>${esc(c.status)}</td><td>${esc(c.notes || "")}</td></tr>`).join("");
  document.getElementById("validation").innerHTML = `
    <h2>验证</h2>
    <table><thead><tr><th>检查项</th><th>状态</th><th>说明</th></tr></thead><tbody>${rows || "<tr><td colspan='3'>未记录验证项。</td></tr>"}</tbody></table>
    <h3>未解决项</h3>
    <ul>${asArray(bundle.validation?.unresolved).map(item => `<li>${esc(item)}</li>`).join("") || "<li>未记录未解决项。</li>"}</ul>
  `;
}

function setupSearch() {
  const input = document.getElementById("searchInput");
  input.addEventListener("input", () => {
    const q = input.value.trim().toLowerCase();
    document.querySelectorAll(".searchable").forEach(node => {
      node.classList.toggle("hidden-by-search", Boolean(q) && !node.textContent.toLowerCase().includes(q));
    });
  });
}

function setupNav() {
  const links = [...document.querySelectorAll(".nav a")];
  const sections = links.map(a => document.querySelector(a.getAttribute("href")));
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      links.forEach(a => a.classList.toggle("active", a.getAttribute("href") === `#${entry.target.id}`));
    });
  }, { rootMargin: "-30% 0px -60% 0px" });
  sections.forEach(section => section && observer.observe(section));
}

async function main() {
  try {
    const bundle = await loadBundle();
    const title = bundle.intake?.paper?.title || "论文与源码联合分析";
    document.title = title;
    document.getElementById("pageTitle").textContent = title;
    document.getElementById("brandTitle").textContent = (title.split(":")[0] || "Paper-Code").slice(0, 24);
    document.getElementById("subtitle").textContent = `${bundle.intake?.repository?.path_or_url || ""} ${bundle.intake?.repository?.commit || ""}`.trim();
    renderSummary(bundle);
    await renderReport();
    await renderQuestions(bundle);
    renderMechanisms(bundle);
    renderExperiments(bundle);
    renderOmissions(bundle);
    await renderDiagrams(bundle);
    renderModify(bundle);
    renderValidation(bundle);
    setupSearch();
    setupNav();
  } catch (err) {
    document.getElementById("summary").innerHTML = `<h2>加载失败</h2><p class="note">${esc(err.message)}</p><p>请用本地 HTTP 服务打开本页，例如在分析目录运行 <code>python -m http.server 8780</code> 后访问 <code>/site/index.html</code>。</p>`;
  }
}

main();
