
import json
import re
from pathlib import Path
from typing import Dict, Any, Tuple

from marker.converters.pdf import PdfConverter
from marker.renderers.markdown import MarkdownRenderer
from marker.models import create_model_dict
from marker.output import text_from_rendered
from marker.schema import BlockTypes


class PosterGenParserUnit:
    def __init__(self):
        self.name = "PosterGenParserUnit"
        print(f"Initializing {self.name}")
        
        config = {
            "recognition_batch_size": 4,
            "layout_batch_size": 4,
            "detection_batch_size": 4,
            "table_rec_batch_size": 4,
            "ocr_error_batch_size": 4,
            "equation_batch_size": 4,
            "disable_tqdm": False,
        }

        self.model_dict = create_model_dict()
        self.converter = PdfConverter(artifact_dict=self.model_dict, config=config)
        self.clean_pattern = re.compile(r"<!--[\s\S]*?-->")

    def parse(self, pdf_path: str, output_dir: str) -> Dict:
        print(f"[{self.name}] Starting parsing for: {pdf_path}")

        out = Path(output_dir)
        assets = out / "assets"
        out.mkdir(parents=True, exist_ok=True)
        assets.mkdir(parents=True, exist_ok=True)

        text, result = self._extract_raw_text(pdf_path, out)
        figures, tables = self._extract_assets(result, assets)

        print(f"[{self.name}] Successfully extracted raw text, {len(figures)} images, and {len(tables)} tables.")
        
        return {
            "raw_text_path": str(out / "raw.md"),
            "figures_path": str(assets / "figures.json"),
            "tables_path": str(assets / "tables.json"),
            "figure_count": len(figures),
            "table_count": len(tables)
        }

    def parse_markdown(self, md_path: str, output_dir: str) -> Dict:
        """
        仅基于现有 Markdown 文件进行兼容处理：
        - 拷贝/写入到 output_dir/raw.md
        - 创建空的 figures.json / tables.json
        - 返回与 parse() 一致的结果字典，计数为 0
        """
        print(f"[{self.name}] Using existing Markdown (no PDF): {md_path}")
        
        source = Path(md_path)
        if not source.exists():
            raise FileNotFoundError(f"Markdown file not found: {md_path}")

        out = Path(output_dir)
        assets = out / "assets"
        out.mkdir(parents=True, exist_ok=True)
        assets.mkdir(parents=True, exist_ok=True)

        target = out / "raw.md"
        text = source.read_text(encoding="utf-8")
        text = self.clean_pattern.sub("", text)
        target.write_text(text, encoding="utf-8")

        (assets / "figures.json").write_text("{}", encoding="utf-8")
        (assets / "tables.json").write_text("{}", encoding="utf-8")

        print(f"[{self.name}] Markdown copied. No figures/tables extracted.")
        return {
            "raw_text_path": str(target),
            "figures_path": str(assets / "figures.json"),
            "tables_path": str(assets / "tables.json"),
            "figure_count": 0,
            "table_count": 0,
        }

    def _extract_raw_text(self, pdf_path: str, content_dir: Path) -> Tuple[str, Any]:
        print(f"[{self.name}] Converting PDF to raw text...")
        document = self.converter.build_document(pdf_path)

        renderer = self.converter.resolve_dependencies(MarkdownRenderer)
        rendered = renderer(document)

        text, _, images = text_from_rendered(rendered)
        text = self.clean_pattern.sub("", text)

        (content_dir / "raw.md").write_text(text, encoding="utf-8")

        print(f"[{self.name}] Extracted {len(text)} characters of text.")

        return text, (document, rendered, images)

    def _extract_assets(self, result, assets_dir: Path) -> Tuple[Dict, Dict]:
        print(f"[{self.name}] Extracting assets (figures and tables)...")

        document, rendered, marker_images = result
        caption_map = self._extract_captions(document)

        figures = {}
        tables = {}
        img_cnt = 0
        tab_cnt = 0

        for img_name, pil_image in marker_images.items():
            info = caption_map.get(img_name, {'captions': [], 'block_type': 'Unknown'})

            if 'table' in img_name.lower() or 'Table' in img_name or info.get('block_type') == 'Table':
                tab_cnt += 1
                path = assets_dir / f"table-{tab_cnt}.png"
                pil_image.save(path, "PNG")

                tables[str(tab_cnt)] = {
                    'caption': info['captions'][0] if info['captions'] else f"Table {tab_cnt}",
                    'path': str(path),
                    'width': pil_image.width,
                    'height': pil_image.height,
                    'aspect': pil_image.width / pil_image.height if pil_image.height > 0 else 1,
                }
            else:
                img_cnt += 1
                path = assets_dir / f"figure-{img_cnt}.png"
                pil_image.save(path, "PNG")

                figures[str(img_cnt)] = {
                    'caption': info['captions'][0] if info['captions'] else f"Figure {img_cnt}",
                    'path': str(path),
                    'width': pil_image.width,
                    'height': pil_image.height,
                    'aspect': pil_image.width / pil_image.height if pil_image.height > 0 else 1,
                }

        with open(assets_dir / "figures.json", 'w', encoding='utf-8') as f:
            json.dump(figures, f, indent=2)
        with open(assets_dir / "tables.json", 'w', encoding='utf-8') as f:
            json.dump(tables, f, indent=2)
        with open(assets_dir / "fig_tab_caption_mapping.json", 'w', encoding='utf-8') as f:
            json.dump(caption_map, f, indent=2, ensure_ascii=False)

        return figures, tables

    def _extract_captions(self, document):
        caption_map = {}
        for page in document.pages:
            for block_id in page.structure:
                block = page.get_block(block_id)

                if block.block_type in [BlockTypes.FigureGroup, BlockTypes.TableGroup, BlockTypes.PictureGroup]:
                    child_blocks = block.structure_blocks(page)
                    figure_or_table = None
                    captions = []
                    for child in child_blocks:
                        child_block = page.get_block(child)
                        if child_block.block_type in [BlockTypes.Figure, BlockTypes.Table, BlockTypes.Picture]:
                            figure_or_table = child_block
                        elif child_block.block_type in [BlockTypes.Caption, BlockTypes.Footnote]:
                            captions.append(child_block.raw_text(document))
                    
                    if figure_or_table:
                        image_filename = f"{figure_or_table.id.to_path()}.jpeg"
                        caption_map[image_filename] = {
                            'block_id': str(figure_or_table.id),
                            'block_type': str(figure_or_table.block_type),
                            'captions': captions,
                            'page': page.page_id
                        }
                
                elif block.block_type in [BlockTypes.Figure, BlockTypes.Table, BlockTypes.Picture]:
                    image_filename = f"{block.id.to_path()}.jpeg"
                    if image_filename not in caption_map:
                        nearby_captions = self._find_nearby_captions(page, block, document)
                        caption_map[image_filename] = {
                            'block_id': str(block.id),
                            'block_type': str(block.block_type),
                            'captions': nearby_captions,
                            'page': page.page_id
                        }
        return caption_map

    def _find_nearby_captions(self, page, target_block, document):
        captions = []
        for block_id in page.structure:
            block = page.get_block(block_id)
            if block.block_type in [BlockTypes.Caption, BlockTypes.Text]:
                caption_text = block.raw_text(document)
                if any(keyword in caption_text for keyword in ['Figure', 'Table', 'Fig.']):
                    captions.append(caption_text)
        
        if not captions:
            for block in [page.get_prev_block(target_block), page.get_next_block(target_block)]:
                if block and block.block_type in [BlockTypes.Caption, BlockTypes.Text]:
                    caption_text = block.raw_text(document)
                    if any(keyword in caption_text for keyword in ['Figure', 'Table', 'Fig.']):
                        captions.append(caption_text)
        return captions
