
import json
import os
import markdown
from pathlib import Path
from typing import Any, Dict, List
import requests
import re

try:
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover
    OpenAI = None  # lazy import fallback

class PosterGenRendererUnit:
    def __init__(self):
        self.name = "PosterGenRendererUnit"
        print(f"Initializing {self.name}")

    def render(self, parser_results: dict, output_dir: str, mode: str = "llm", model_id: str = None, temperature: float = None, max_tokens: int = None, max_attempts: int = None, template_name: str = None):
        """
        Renders the parsed content into an HTML file.
        mode: "llm" (default) to render via LLM with doubao template, or "simple" to use basic preview.
        """
        print(f"[{self.name}] Starting rendering process...")
        output_path = Path(output_dir)
        # Ensure output directory exists
        if not output_path.exists():
            output_path.mkdir(parents=True, exist_ok=True)
        else:
            # Clean up old HTML render results to avoid confusion in the output folder
            # This ensures that only the currently generated HTMLs are present.
            for old_html in output_path.glob("poster_llm*.html"):
                try:
                    old_html.unlink()
                except Exception as e:
                    print(f"[{self.name}] Warning: Failed to delete old file {old_html}: {e}")
            # Also clean up preview if exists
            preview_html = output_path / "poster_preview.html"
            if preview_html.exists():
                 try:
                    preview_html.unlink()
                 except Exception:
                    pass

        # Define paths from parser results
        raw_text_path = Path(parser_results['raw_text_path'])
        figures_path = Path(parser_results.get('figures_path', Path(output_path / 'assets' / 'figures.json')))
        tables_path = Path(parser_results.get('tables_path', Path(output_path / 'assets' / 'tables.json')))
        web_images_path = Path(parser_results.get('web_images_path', Path(output_path / 'assets' / 'web_images.json')))

        if not raw_text_path.exists():
            print(f"[{self.name}] Error: Markdown file not found at {raw_text_path}")
            return None

        # Read content from files
        raw_text = raw_text_path.read_text(encoding='utf-8')
        if figures_path.exists():
            try:
                with open(figures_path, 'r', encoding='utf-8') as f:
                    figures = json.load(f)
            except Exception as e:
                print(f"[{self.name}] Warning: Failed to load figures from {figures_path}: {e}")
                figures = {}
        else:
            figures = {}
        if tables_path.exists():
            try:
                with open(tables_path, 'r', encoding='utf-8') as f:
                    tables = json.load(f)
            except Exception as e:
                print(f"[{self.name}] Warning: Failed to load tables from {tables_path}: {e}")
                tables = {}
        else:
            tables = {}
        # 读取自动下载的网页图片
        # 如果 parser_results 中没有 web_images_path，说明本次运行没有启用自动图片功能
        # 此时不应该加载任何可能存在的旧 web_images.json 文件
        if 'web_images_path' in parser_results and web_images_path.exists():
            try:
                with open(web_images_path, 'r', encoding='utf-8') as f:
                    web_images = json.load(f)
            except Exception:
                web_images = []
        else:
            web_images = []

        mode = (mode or "llm").lower()
        if mode == "llm":
            try:
                # 优先使用 template_name 参数或环境变量 POSTER_TEMPLATE
                # 如果两者有其一，则使用该特定模板进行渲染
                target_template = template_name or os.getenv("POSTER_TEMPLATE")
                
                if target_template:
                    # 单模板渲染模式
                    print(f"[{self.name}] Using specified template: {target_template}")
                    html = self._render_via_llm(output_path, raw_text, figures, tables, web_images, model_id=model_id, temperature=temperature, max_tokens=max_tokens, max_attempts=max_attempts, template_name=target_template)
                    
                    # 使用模板名称作为输出文件名的一部分，或者保持默认 poster_llm.html
                    # 为了避免歧义，如果指定了具体路径，我们尝试提取文件名；如果是默认逻辑，使用 poster_llm.html
                    stem = Path(target_template).stem
                    if stem == "doubao": # default behavior compat
                        out_name = "poster_llm.html"
                    else:
                        out_name = f"poster_llm__{stem}.html"
                        
                    html_output_path = output_path / out_name
                    html = self._postprocess_references(html, raw_text)
                    html_output_path.write_text(self._postprocess_html(html), encoding='utf-8')
                    print(f"[{self.name}] Successfully rendered HTML poster via LLM to: {html_output_path}")
                    return str(html_output_path)
                else:
                    # 未指定模板，扫描所有 .txt 模板并渲染（多模板模式）
                    template_files = self._list_templates()
                    if not template_files:
                        # 兜底：使用默认 doubao.txt
                        print(f"[{self.name}] No templates found or specified, falling back to default.")
                        template_html = self._load_doubao_template()
                        html = self._render_via_llm_with_template(template_html, output_path, raw_text, figures, tables, web_images, model_id=model_id, temperature=temperature, max_tokens=max_tokens, max_attempts=max_attempts)
                        html_output_path = output_path / "poster_llm.html"
                        html = self._postprocess_references(html, raw_text)
                        html_output_path.write_text(self._postprocess_html(html), encoding='utf-8')
                        print(f"[{self.name}] Successfully rendered HTML poster via LLM to: {html_output_path}")
                        return str(html_output_path)
                    
                    print(f"[{self.name}] No specific template specified, rendering all {len(template_files)} templates found...")
                    rendered_paths = []
                    for path in template_files:
                        template_html = Path(path).read_text(encoding='utf-8')
                        html = self._render_via_llm_with_template(template_html, output_path, raw_text, figures, tables, web_images, model_id=model_id, temperature=temperature, max_tokens=max_tokens, max_attempts=max_attempts)
                        html = self._postprocess_references(html, raw_text)
                        out_name = f"poster_llm__{Path(path).stem}.html"
                        out_path = output_path / out_name
                        out_path.write_text(self._postprocess_html(html), encoding='utf-8')
                        print(f"[{self.name}] Rendered via LLM with template '{Path(path).name}' -> {out_path}")
                        rendered_paths.append(str(out_path))
                    return rendered_paths
            except Exception as e:
                print(f"[{self.name}] LLM rendering failed, falling back to simple preview. Error: {e}")
                import traceback
                traceback.print_exc()
                # fall through to simple mode

        # simple preview rendering
        final_html = self._render_simple(raw_text, figures, tables, web_images)
        html_output_path = output_path / "poster_preview.html"
        html_output_path.write_text(final_html, encoding='utf-8')
        print(f"[{self.name}] Successfully rendered HTML poster to: {html_output_path}")
        return str(html_output_path)

    def _render_simple(self, raw_text: str, figures: Dict[str, Any], tables: Dict[str, Any], web_images: list) -> str:
        """
        非三栏的自然排版：选取一张 Hero 图置于顶部，其余根据与章节的简单语义匹配插入到对应段落下方；
        原生的 figures/tables 作为附录展示，避免生硬分栏。
        """
        html_template = self._get_html_template()

        # 1) 按标题切分章节
        sections = []
        current = {"heading": None, "level": 0, "lines": []}
        for ln in raw_text.splitlines():
            m = re.match(r"^(#{1,6})\s+(.*)$", ln.strip())
            if m:
                if current["heading"] is not None or current["lines"]:
                    sections.append(current)
                current = {"heading": m.group(2).strip(), "level": len(m.group(1)), "lines": []}
            else:
                current["lines"].append(ln)
        if current["heading"] is not None or current["lines"]:
            sections.append(current)
        if not sections:
            sections = [{"heading": None, "level": 0, "lines": raw_text.splitlines()}]

        # 2) 选 Hero + 其余分配
        def area_score(w: dict) -> float:
            return float(w.get("width") or 0) * float(w.get("height") or 0)
        def composite_score(w: dict) -> float:
            return float(w.get("score") or 0.0) * 10.0 + area_score(w)
        valid_web = [w for w in web_images if (w.get("image_url") or w.get("rel_path"))]
        hero_html = ""
        if valid_web:
            valid_web.sort(key=composite_score, reverse=True)
            top = valid_web[0]
            hero_url = top.get("image_url") or top.get("rel_path") or ""
            hero_title = top.get("title") or top.get("keyword") or "Hero"
            hero_html = f"""
            <div class="hero-banner">
                <img src="{hero_url}" alt="{hero_title}">
                <div class="hero-caption">{hero_title}</div>
            </div>
            """
            remaining = valid_web[1:]
        else:
            remaining = []

        # 3) 简单语义匹配：根据标题/正文 token 与图片标题/关键词/域名交集选择最佳章节
        def tokenize(s: str) -> set:
            if not s:
                return set()
            toks = set()
            for w in re.findall(r"[A-Za-z][A-Za-z0-9_\-]{1,}", s.lower()):
                toks.add(w)
            for seg in re.findall(r"[\u4e00-\u9fff]{1,}", s):
                toks |= set(list(seg))
            return toks
        section_tokens = []
        for sec in sections:
            tokens = tokenize((sec["heading"] or "") + " " + "\n".join(sec["lines"]))
            section_tokens.append(tokens)

        assigned = {i: [] for i in range(len(sections))}
        for w in remaining:
            tokens = tokenize((w.get("title") or "") + " " + (w.get("keyword") or "") + " " + (w.get("domain") or ""))
            best_idx, best_overlap = 0, -1
            for idx, tok in enumerate(section_tokens):
                overlap = len(tokens & tok)
                if overlap > best_overlap:
                    best_idx, best_overlap = idx, overlap
            assigned[best_idx].append(w)

        # 4) 生成正文 + 分节图集
        article_parts = []
        for idx, sec in enumerate(sections):
            md_block = ""
            if sec["heading"] is not None:
                md_block += ("#" * max(1, sec["level"])) + " " + sec["heading"] + "\n\n"
            if sec["lines"]:
                md_block += "\n".join(sec["lines"])
            html_block = markdown.markdown(md_block) if md_block.strip() else ""

            imgs_html = ""
            for w in assigned.get(idx, []):
                url = w.get("image_url") or w.get("rel_path") or ""
                title = w.get("title") or w.get("keyword") or ""
                width = w.get("width") or 0
                height = w.get("height") or 0
                ratio_class = "square"
                try:
                    if width and height:
                        aspect = float(width) / float(height)
                        ratio_class = "landscape" if aspect >= 1.3 else ("portrait" if aspect <= 0.77 else "square")
                except Exception:
                    ratio_class = "square"
                imgs_html += f"""
                <div class="gallery-item {ratio_class}">
                    <img src="{url}" alt="{title}">
                    <p class="caption">{title}</p>
                </div>
                """
            if imgs_html:
                imgs_html = f'<div class="gallery-grid">{imgs_html}\n</div>'
            article_parts.append(html_block + imgs_html)

        # 5) 附录：原生 figures/tables
        appendix = ""
        if figures:
            fig_html = ""
            for fig_id, fig_data in figures.items():
                img_path = Path(fig_data['path'])
                rel = Path('assets') / img_path.name
                fig_html += f"""
                <div class="gallery-item">
                    <img src="{rel}" alt="{fig_data.get('caption','')}">
                    <p class="caption"><strong>Figure {fig_id}</strong> {fig_data.get('caption','')}</p>
                </div>
                """
            if fig_html:
                appendix += f'<h2>Figures</h2><div class="gallery-grid">{fig_html}</div>'
        if tables:
            tab_html = ""
            for tab_id, tab_data in tables.items():
                img_path = Path(tab_data['path'])
                rel = Path('assets') / img_path.name
                tab_html += f"""
                <div class="gallery-item">
                    <img src="{rel}" alt="{tab_data.get('caption','')}">
                    <p class="caption"><strong>Table {tab_id}</strong> {tab_data.get('caption','')}</p>
                </div>
                """
            if tab_html:
                appendix += f'<h2>Tables</h2><div class="gallery-grid">{tab_html}</div>'

        article_content = "\n".join([p for p in article_parts if p.strip()]) + (("\n" + appendix) if appendix else "")
        return html_template.format(hero_content=hero_html, article_content=article_content)

    def _render_via_llm(self, output_path: Path, raw_text: str, figures: Dict[str, Any], tables: Dict[str, Any], web_images: list, model_id: str = None, temperature: float = None, max_tokens: int = None, max_attempts: int = None, template_name: str = None) -> str:
        template_html = self._load_doubao_template(template_name)
        return self._render_via_llm_with_template(template_html, output_path, raw_text, figures, tables, web_images, model_id=model_id, temperature=temperature, max_tokens=max_tokens, max_attempts=max_attempts)

    def _render_via_llm_with_template(self, template_html: str, output_path: Path, raw_text: str, figures: Dict[str, Any], tables: Dict[str, Any], web_images: list, model_id: str = None, temperature: float = None, max_tokens: int = None, max_attempts: int = None) -> str:
        assets: List[Dict[str, Any]] = []
        for fig_id, fig in figures.items():
            assets.append({
                "type": "figure",
                "id": fig_id,
                "caption": fig.get("caption", ""),
                "rel_path": str(Path('assets') / Path(fig.get('path', '')).name),
                "width": fig.get("width"),
                "height": fig.get("height"),
                "aspect": fig.get("aspect")
            })
        for tab_id, tab in tables.items():
            assets.append({
                "type": "table",
                "id": tab_id,
                "caption": tab.get("caption", ""),
                "rel_path": str(Path('assets') / Path(tab.get('path', '')).name),
                "width": tab.get("width"),
                "height": tab.get("height"),
                "aspect": tab.get("aspect")
            })
        # 新增：网页图片作为一种资产类型，供 LLM 自行布局使用（允许使用 image_url 外链）
        for idx, w in enumerate(web_images):
            rel_path = w.get("rel_path") or ""
            image_url = w.get("image_url") or ""
            assets.append({
                "type": "web_image",
                "id": f"web_{idx+1}",
                "caption": w.get("title") or w.get("keyword") or f"Image {idx+1}",
                "rel_path": rel_path,
                "image_url": image_url,
                "width": w.get("width"),
                "height": w.get("height"),
                "score": w.get("score"),
                "source": w.get("source"),
                "domain": w.get("domain"),
            })

        model = model_id or os.getenv("TEXT_MODEL") or "gpt-4.1-2025-04-14"
        temp = 0.7 if temperature is None else float(temperature)
        tokens = 8192 if max_tokens is None else int(max_tokens)
        attempts = 3 if max_attempts is None else int(max_attempts)

        system_prompt = (
            "你是专业的学术海报前端设计助手。根据提供的论文文本与素材列表，"
            "生成一个完整且可直接打开的 HTML 页面。必须：\n"
            "1) 参考给定 template_html 的信息架构和视觉风格（Tailwind/字体/图标等引入保持一致或兼容）；\n"
            "2) 将 figures/tables 按 rel_path 正确插入页面；\n"
            "2.1) 你还会收到 web_image 类型的资产（从搜索引擎自动获取），其字段包含 image_url 与 rel_path，"
            "对 web_image 优先使用 image_url 外链渲染（仅当 image_url 不可用时再使用 rel_path）。"
            "请结合 score/标题/上下文合理挑选与排版，避免堆叠过多，精选其一或数张增强视觉；\n"
            "3) 合理组织内容结构（标题、要点卡片、图表区等），保持可读性与审美；\n"
            "4) **引用与链接（非常重要）**：\n"
            "   a) 正文中每个引用了具体来源的句子末尾，"
            "用 <a class=\"cite-ref\" href=\"真实URL\" target=\"_blank\">[N]</a> 标注内联引用，"
            "href 直接填写该来源的真实 URL，N 从 1 递增。\n"
            "   b) **URL 严禁编造！必须原样复制自提供的原始文本中出现的 URL。** "
            "如果原文中找不到 URL，则不要添加该引用角标。\n"
            "   c) 同一来源多次被引用时，复用同一个编号和 URL。\n"
            "   d) **不要生成底部的 references / 参考文献列表。** 所有引用仅以正文中的角标形式存在。\n"
            "5) 仅输出 HTML 源码，不要附加解释。"
        )

        user_payload = {
            "template_html": template_html,
            "paper_text": raw_text,
            "assets": assets
        }

        # 检查是否为 Gemini 模型，若是则走原生调用逻辑
        if "gemini" in model.lower():
            print(f"[{self.name}] Detected Gemini model '{model}', switching to native API.")
            return self._call_gemini_native(
                model=model,
                system_prompt=system_prompt,
                user_payload=user_payload,
                temperature=temp,
                max_tokens=tokens, # Pass the (potentially larger) token limit
                attempts=attempts
            )

        # 首选：通过 HTTP 直连兼容的 Chat Completions 接口（参考 curl 示例）
        base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("RUNWAY_API_BASE") or "https://runway.devops.xiaohongshu.com/openai"
        api_version = os.getenv("RUNWAY_API_VERSION") or "2024-12-01-preview"
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("RUNWAY_API_KEY")

        http_err: Exception | None = None
        if api_key:
            endpoint = f"{base_url.rstrip('/')}/chat/completions?api-version={api_version}"
            headers = {
                "api-key": api_key,
                "Content-Type": "application/json",
            }
            body = {
                "model": model,
                "temperature": temp,
                "max_tokens": tokens,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)}
                ],
            }

            for _ in range(max(1, attempts)):
                try:
                    r = requests.post(endpoint, headers=headers, json=body, timeout=60)
                    if r.status_code < 200 or r.status_code >= 300:
                        raise RuntimeError(f"HTTP {r.status_code}: {r.text[:500]}")
                    data = r.json()
                    choices = data.get("choices") or []
                    content = (choices[0].get("message", {}).get("content") if choices else "") or ""
                    if not content:
                        raise RuntimeError("empty completion content")
                    content = self._strip_code_fences(content)
                    return content
                except Exception as e:  # pragma: no cover
                    http_err = e

        # 回退方案：如果提供了 openai SDK 配置，尝试 SDK
        client = self._init_llm_client()
        if client is not None:
            last_err: Exception | None = None
            for _ in range(max(1, attempts)):
                try:
                    resp = client.chat.completions.create(
                        model=model,
                        temperature=temp,
                        max_tokens=tokens,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)}
                        ],
                    )
                    content = resp.choices[0].message.content if resp and resp.choices else ""
                    if not content:
                        raise RuntimeError("empty completion content")
                    content = self._strip_code_fences(content)
                    return content
                except Exception as e:  # pragma: no cover
                    last_err = e
            raise RuntimeError(f"LLM generation failed after {attempts} attempts: {last_err}")

        raise RuntimeError(f"HTTP client not configured (missing api key). Last error: {http_err}")

    def _call_gemini_native(self, model: str, system_prompt: str, user_payload: dict, temperature: float, max_tokens: int, attempts: int) -> str:
        """
        调用 Gemini 原生 API (https://runway.devops.rednote.life/openai/google/v1:generateContent)。
        逻辑参照 PosterGen2/dev/APIconn_test.py。
        """
        endpoint = "https://runway.devops.rednote.life/openai/google/v1:generateContent"
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("RUNWAY_API_KEY")
        if not api_key:
             raise RuntimeError("missing RUNWAY_API_KEY/OPENAI_API_KEY for Gemini call")

        headers = {
            "api-key": api_key,
            "Content-Type": "application/json",
        }
        
        # Gemini 原生 API 支持 systemInstruction
        # 但为了简单兼容，我们把 system prompt 拼接到 user content 或者作为 systemInstruction 传入
        # 根据 test.sh 示例，可以使用 systemInstruction 字段
        
        # 构造 user content 文本
        user_text = json.dumps(user_payload, ensure_ascii=False)
        
        payload = {
            "contents": [{
                "role": "user",
                "parts": [{"text": user_text}]
            }],
            "systemInstruction": {
                "parts": [{"text": system_prompt}]
            },
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
                "topP": 1,
            }
        }

        last_err: Exception | None = None
        for _ in range(max(1, attempts)):
            try:
                resp = requests.post(endpoint, headers=headers, json=payload, timeout=120)
                if resp.status_code < 200 or resp.status_code >= 300:
                     raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:800]}")
                
                res_json = resp.json()
                
                # 错误检查
                if "error" in res_json:
                     raise RuntimeError(f"API Error: {res_json.get('error')}")

                if "candidates" not in res_json or not res_json["candidates"]:
                     raise RuntimeError(f"No candidates returned. Full response: {res_json}")

                candidate = res_json["candidates"][0]
                finish_reason = candidate.get("finishReason")
                if finish_reason and finish_reason != "STOP":
                     print(f"[{self.name}] Warning: Gemini finishReason is {finish_reason}.")

                parts = candidate.get("content", {}).get("parts", [])
                if not parts:
                     raise RuntimeError(f"No parts in response content. Finish reason: {finish_reason}. Full response: {res_json}")
                     
                answer = parts[0].get("text", "")
                if not answer:
                    raise RuntimeError(f"empty response text from Gemini. Full response: {res_json}")
                
                return self._strip_code_fences(answer)

            except Exception as e:
                last_err = e
        
        raise RuntimeError(f"Gemini native call failed: {last_err}")

    def _init_llm_client(self):
        if OpenAI is None:
            return None
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        if not api_key:
            return None
        if base_url:
            return OpenAI(api_key=api_key, base_url=base_url)
        return OpenAI(api_key=api_key)

    # ------------------------------------------------------------------
    #  Reference post-processing: verify URLs & replace inline citations
    # ------------------------------------------------------------------

    _URL_RE = re.compile(
        r'https?://[^\s\)\]>"\'，。、；：！？）】」』\u3000<]+'
    )

    @staticmethod
    def _extract_source_urls(raw_text: str) -> set:
        """Extract every URL that appears in the original source text."""
        urls = set()
        for m in PosterGenRendererUnit._URL_RE.finditer(raw_text):
            urls.add(m.group(0).rstrip('/.,;:!?'))
        return urls

    @staticmethod
    def _url_verified(url: str, source_urls: set) -> bool:
        """Strict check: URL (after normalisation) must appear in source."""
        clean = url.rstrip('/.,;:!?')
        return any(clean == s for s in source_urls)

    @staticmethod
    def _postprocess_references(html: str, raw_text: str) -> str:
        """Verify every inline citation URL against the original source text.

        - Verified: keep the clickable ``<a class="cite-ref">`` as-is.
        - Unverified (hallucinated / placeholder): remove the entire tag.
        """
        if not raw_text:
            return html

        source_urls = PosterGenRendererUnit._extract_source_urls(raw_text)
        if not source_urls:
            # No URLs in source → strip all cite-ref tags
            html = re.sub(
                r'<a\b[^>]*class="cite-ref"[^>]*>.*?</a>',
                '', html, flags=re.IGNORECASE,
            )
            return html

        def _check(m: re.Match) -> str:
            tag = m.group(0)
            href_m = re.search(r'href=["\'](https?://[^"\']+)["\']', tag)
            if href_m and PosterGenRendererUnit._url_verified(href_m.group(1), source_urls):
                return tag  # keep
            return ''  # remove

        html = re.sub(
            r'<a\b[^>]*class="cite-ref"[^>]*>.*?</a>',
            _check, html, flags=re.IGNORECASE,
        )
        return html

    @staticmethod
    def _postprocess_html(html: str) -> str:
        """Inject AOS graceful-degradation: content visible by default,
        animations activate only after AOS loads successfully."""
        AOS_FALLBACK = (
            '\n<!-- AOS graceful degradation -->\n'
            '<style id="aos-fallback">\n'
            '  [data-aos] { opacity: 1 !important; transform: none !important; transition: none !important; }\n'
            '</style>\n'
        )
        AOS_ACTIVATE = (
            '\n<script>\n'
            '// Remove fallback only if AOS loaded — let original AOS.init() handle animations\n'
            '(function(){\n'
            '  var fb = document.getElementById("aos-fallback");\n'
            '  if (typeof AOS !== "undefined" && fb) fb.remove();\n'
            '})();\n'
            '</script>\n'
        )
        # Inject fallback style right before </head>
        if '</head>' in html:
            html = html.replace('</head>', AOS_FALLBACK + '</head>', 1)
        # Inject activation script right before </body>
        if '</body>' in html:
            html = html.replace('</body>', AOS_ACTIVATE + '</body>', 1)
        return html

    def _strip_code_fences(self, text: str) -> str:
        """
        去除形如 ```html ... ``` 或 ``` ... ``` 的最外层代码块包裹。
        仅清理首尾围栏，不影响正文内部内容。
        """
        if not text:
            return text
        t = text.strip()
        # 去首部围栏：``` 或 ```lang
        t = re.sub(r"^\s*```[a-zA-Z0-9_-]*\s*\n", "", t)
        # 去尾部围栏：```
        t = re.sub(r"\n?\s*```\s*$", "", t)
        return t.strip()

    def _load_doubao_template(self, template_name: str = None) -> str:
        templates_dir = Path(__file__).parent / "templates"
        # 允许通过参数或环境变量选择模板文件名或绝对路径，默认 doubao.txt
        name = template_name or os.getenv("POSTER_TEMPLATE") or "doubao.txt"
        
        candidate_path = Path(name)
        # 如果是绝对路径，直接使用
        if candidate_path.is_absolute():
            template_path = candidate_path
        # 如果没有指定后缀，默认追加 .txt
        elif not name.endswith(".txt"):
             template_path = templates_dir / f"{name}.txt"
        else:
            template_path = templates_dir / name
            
        if not template_path.exists():
            # 只有当用户显式指定了 POSTER_TEMPLATE 或 template_name 时才严格报错
            # 如果仅仅是默认值 "doubao.txt" 找不到，可能还是需要报错，因为这是兜底逻辑
            raise FileNotFoundError(f"template not found at {template_path}")
            
        return template_path.read_text(encoding='utf-8')

    def _list_templates(self) -> list:
        """扫描 templates 目录，返回所有 .txt 模板的完整路径列表。"""
        templates_dir = Path(__file__).parent / "templates"
        if not templates_dir.exists():
            return []
        return [str(p) for p in templates_dir.glob("*.txt")]

    def _get_html_template(self) -> str:
        """单列自然排版模板（Hero + 正文 + 图集样式）。"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Poster Preview</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f8f9fa;
            color: #212529;
        }
        .container {
            max-width: 1100px;
            margin: 0 auto;
            padding: 24px;
        }
        .header {
            text-align: center;
            margin-bottom: 8px;
            border-bottom: 2px solid #dee2e6;
            padding-bottom: 10px;
        }
        .caption {
            font-style: italic;
            color: #6c757d;
            margin-top: 8px;
            font-size: 0.9em;
        }
        img {
            max-width: 100%;
            height: auto;
            border-radius: 6px;
            border: 1px solid #e9ecef;
        }
        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 14px;
            margin: 10px 0 24px 0;
        }
        .gallery-item {
            background: #fff;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .gallery-item.landscape { grid-column: span 2; }
        .gallery-item.portrait { grid-row: span 2; }
        .hero-banner {
            width: 100%;
            border-radius: 12px;
            overflow: hidden;
            margin: 16px 0 24px 0;
            position: relative;
            border: 1px solid #e9ecef;
        }
        .hero-banner img {
            width: 100%;
            height: auto;
            display: block;
        }
        .hero-caption {
            position: absolute;
            left: 12px;
            bottom: 12px;
            background: rgba(0,0,0,0.55);
            color: #fff;
            padding: 6px 10px;
            border-radius: 6px;
            font-size: 0.95em;
        }
        .article {
            background: #fff;
            border: 1px solid #dee2e6;
            border-radius: 10px;
            padding: 18px 20px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        }
        .article h1, .article h2, .article h3 {
            color: #3c4043;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Poster Content Preview</h1>
        </div>
        {hero_content}
        <div class="article">
            {article_content}
        </div>
    </div>
</body>
</html>
"""
