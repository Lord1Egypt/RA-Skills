import re
import requests
import xml.etree.ElementTree as ET


class ArxivClient:
    NS_ATOM = 'http://www.w3.org/2005/Atom'
    NS_ARXIV = 'http://arxiv.org/schemas/atom'

    def parse_id(self, url_or_id):
        """从各种格式中提取 arxiv ID（不含版本号）"""
        s = (url_or_id or '').strip()
        # arxiv.org URL 格式
        m = re.search(r'arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]+)', s)
        if m:
            return m.group(1)
        # 纯 ID 或 arxiv:ID 格式
        m = re.match(r'^(?:arxiv:)?([0-9]{4}\.[0-9]+)', s, re.IGNORECASE)
        if m:
            return m.group(1)
        return None

    def fetch_metadata(self, arxiv_id):
        url = f'http://export.arxiv.org/api/query?id_list={arxiv_id}'
        try:
            r = requests.get(url, timeout=20)
            r.raise_for_status()
        except requests.RequestException as e:
            return {'success': False, 'error': f'arxiv API 请求失败: {e}'}

        try:
            root = ET.fromstring(r.text)
            ns = self.NS_ATOM
            ans = self.NS_ARXIV

            entry = root.find(f'{{{ns}}}entry')
            if entry is None:
                return {'success': False, 'error': f'arxiv 未找到该论文: {arxiv_id}'}

            title = (entry.findtext(f'{{{ns}}}title', '') or '').strip().replace('\n', ' ')
            abstract = (entry.findtext(f'{{{ns}}}summary', '') or '').strip().replace('\n', ' ')

            authors = [
                a.findtext(f'{{{ns}}}name', '').strip()
                for a in entry.findall(f'{{{ns}}}author')
            ]
            authors = [a for a in authors if a]

            published = entry.findtext(f'{{{ns}}}published', '') or ''
            year = int(published[:4]) if published else None

            cat_el = entry.find(f'{{{ans}}}primary_category')
            category = cat_el.get('term', 'other') if cat_el is not None else 'other'

            return {
                'success': True,
                'title': title,
                'authors': authors,
                'year': year,
                'abstract': abstract,
                'category': category
            }
        except ET.ParseError as e:
            return {'success': False, 'error': f'解析失败: {e}'}

    def download_pdf(self, arxiv_id, output_path):
        for url in [
            f'https://arxiv.org/pdf/{arxiv_id}.pdf',
            f'https://arxiv.org/pdf/{arxiv_id}',
        ]:
            try:
                r = requests.get(url, timeout=60, stream=True)
                if r.status_code == 200:
                    ct = r.headers.get('Content-Type', '')
                    if 'html' in ct.lower():
                        continue  # 跳过 HTML 错误页
                    with open(output_path, 'wb') as f:
                        for chunk in r.iter_content(8192):
                            f.write(chunk)
                    return {'success': True, 'path': output_path}
            except requests.RequestException:
                continue
        return {'success': False, 'error': 'PDF 下载失败，已尝试多个地址'}
