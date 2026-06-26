# HTML Shell Core Structure

# HTML Shell Template

When generating the final HTML report, produce a complete self-contained HTML file using this structure. Replace all `[...]` placeholders with actual content.

    <!DOCTYPE html>
    <!-- kai-report-creator v[version] -->
    <html lang="[lang]" data-template="kai-report-creator" data-version="[version]" data-theme="[theme]">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <meta name="generator" content="kai-report-creator [theme-display] v[version]">
      <meta name="ir-hash" content="sha256:[ir-hash]">
      <title>[title]</title>

      <!-- CDN libraries (add only what's needed; omit if --bundle, inline instead) -->
      <!-- If any :::chart blocks present: -->
      <!-- <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script> -->
      <!-- If any :::code blocks present: -->
      <!-- <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/highlight.js@11/styles/github.min.css"> -->
      <!-- (use github-dark.min.css for dark-tech theme) -->
      <!-- <script src="https://cdn.jsdelivr.net/npm/highlight.js@11/lib/highlight.min.js"></script> -->
      <!-- <script>document.addEventListener('DOMContentLoaded', () => hljs.highlightAll());</script> -->

      <!-- AI Readability Layer 1: Report Summary JSON -->
      <!-- Always present, even if not visible to humans -->
      <script type="application/json" id="report-summary">
      {
        "title": "[title]",
        "author": "[author or empty string]",
        "date": "[date]",
        "abstract": "[abstract from frontmatter, or auto-generate a 1-sentence summary of the report content]",
        "poster_title": "[optional stronger summary-card title; opt-in only when the core judgment should read like a poster headline]",
        "poster_subtitle": "[optional subtitle shown below the poster title; only used when poster_title is present]",
        "poster_note": "[optional one-sentence closing line for the left panel; falls back to a short sentence from abstract]",
        "sections": ["[heading of section 1]", "[heading of section 2]", "..."],
        "kpis": [
          {"label": "[label]", "value": "[display value]", "trend": "[trend text or empty]"}
        ]
      }
      </script>

      <!-- Edit mode (always present) -->
      <div class="edit-hotzone" id="edit-hotzone"></div>
      <button class="edit-toggle" id="edit-toggle" title="Edit mode (E)">✏ Edit</button>

      <!-- Export (always present) -->
      <!-- lang:en labels: "↓ Export" / "🖨 Print / PDF" / "🖥 Save PNG (Desktop)" / "📱 Save PNG (Mobile)" / "💬 IM Image" -->
      <!-- lang:zh labels: "↓ 导出"  / "🖨 打印 / PDF"  / "🖥 保存图片（桌面）"    / "📱 保存图片（手机）"  / "💬 IM 分享长图"   -->
      <div class="export-menu" id="export-menu">
        <button class="export-item" id="export-print">[🖨 Print / PDF|🖨 打印 / PDF]</button>
        <button class="export-item" id="export-png-desktop">[🖥 Save PNG (Desktop)|🖥 保存图片（桌面）]</button>
        <button class="export-item" id="export-png-mobile">[📱 Save PNG (Mobile)|📱 保存图片（手机）]</button>
        <button class="export-item" id="export-im-share">[💬 IM Image|💬 IM 长图]</button>
      </div>
      <button class="export-btn" id="export-btn" title="Export">[↓ Export|↓ 导出]</button>

      <!-- Floating TOC (omit entirely if toc:false) -->
      <!-- TOC label localization: lang:en → aria-label="Contents" / "Table of Contents" / <h4>Contents</h4> -->
      <!--                         lang:zh → aria-label="目录" / "报告目录" / <h4>目录</h4> -->
      <button class="toc-toggle" id="toc-toggle-btn" aria-label="[Contents|目录]" aria-expanded="false">☰</button>
      <nav class="toc-sidebar" id="toc-sidebar" aria-label="[Table of Contents|报告目录]">
        <h4>[Contents|目录]</h4>
        <!-- Generate one <a> per ## heading and one per ### heading in the report -->
        <!-- Example (lang:en): <a href="#section-core-metrics" data-section="Core Metrics">Core Metrics</a> -->
        <!-- For ### heading: add class="toc-h3" -->
        [TOC links generated from all ## and ### headings in the IR]
      </nav>

      <div class="main-with-toc">
        <div class="report-wrapper">

          <!-- Report title and meta -->
          <!-- lang:en card button label: "⊞ Summary" | lang:zh: "⊞ 摘要卡" -->
          <div class="title-row">
            <h1>[title]</h1>
            <button class="card-mode-btn" id="card-mode-btn" title="[Summary card|摘要卡片]">[⊞ Summary|⊞ 摘要卡]</button>
          </div>
          [if abstract: <p class="report-subtitle">[abstract]</p>]
          [if author or date: <p class="report-meta">[author] · [date]</p>]

          <!-- Summary card overlay (always present) — left+right panels injected by buildCard() -->
          <div class="sc-overlay" id="sc-overlay">
            <div class="sc-card" id="sc-card">
              <button class="sc-close" id="sc-close" aria-label="Close">✕</button>
              <!-- .sc-left and .sc-right injected by JS -->
            </div>
          </div>

          <!-- AI Readability Layer 2: Section annotations are on each <section> element -->
          <!-- Rendered sections — each ## becomes: -->
          <!-- <section data-section="[heading]" data-summary="[1-sentence summary]"> -->
          <!--   <h2 id="section-[slug]">[heading]</h2> -->
          <!--   [section content] -->
          <!-- </section> -->

          <!-- Shell metadata contract:
               - Do not pass through Pandoc title metadata such as <header id="title-block-header"> or <p class="date">...</p>; the shell owns title/date metadata. Passing both through creates duplicate date output.
               - Standard shell metadata is: kai-report-creator v[version] [theme].
               - Standard shell emits both visible footer and hidden data-watermark with that string.
               - Degradation is allowed for constrained/custom templates: keep at least one footer or watermark carrier with version/theme metadata.
               - Replace stale prose such as "Generated by kai-report-creator" because it loses version/theme metadata. -->

          [All rendered section content here]

          <!-- Visible footer (deterministic shell metadata only; do not add debug hashes, source notes, or extra prose) -->
          <div class="report-footer">kai-report-creator v[version] [theme]</div>

          <!-- Invisible watermark uses the same deterministic metadata string in the standard shell. -->
          <div style="display:none;visibility:hidden;opacity:0;font-size:0;line-height:0;height:0;overflow:hidden;" aria-hidden="true" data-watermark="kai-report-creator v[version] [theme]">
            kai-report-creator v[version] [theme]
          </div>

        </div>
      </div>
