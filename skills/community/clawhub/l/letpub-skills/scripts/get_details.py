import re
import requests
from bs4 import BeautifulSoup


def get_journal_detail(journal_id: int) -> dict:
    """
    一步到位获取并解析期刊详情

    Args:
        journal_id: 期刊 ID

    Returns:
        解析后的期刊信息字典
    """
    url = f"https://letpub.com.cn/index.php?journalid={journal_id}&page=journalapp&view=detail"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return parse_journal_detail(response.text)


def parse_journal_detail(html_content: str):
    """
    解析期刊详情页 HTML 内容

    Args:
        html_content: 期刊详情页的 HTML 字符串

    Returns:
        解析后的期刊信息字典，字段名与 Journal 类属性对应
    """
    soup = BeautifulSoup(html_content, "html.parser")
    journal = {}

    # 期刊信息表格 - 在 #yxyz_content 中查找所有 table.table_yjfx 中的 tr
    trs = []
    seen = set()
    yxyz_content = soup.select_one('#yxyz_content')
    if yxyz_content:
        for table in yxyz_content.select('table.table_yjfx'):
            for tr in table.find_all('tr'):
                if id(tr) not in seen:
                    seen.add(id(tr))
                    trs.append(tr)
    
    if not trs:
        return journal

    for tr in trs:
        tds = tr.find_all('td')
        if not tds:
            continue

        first_cell_text = tds[0].get_text(strip=True)

        if '期刊名字' in first_cell_text:
            # 期刊名
            name_tag = tr.select_one('td:nth-child(2) > span:nth-child(1) > a')
            if name_tag:
                journal['name'] = name_tag.get_text(strip=True)
            # 简称
            shortname_tag = tr.select_one('td:nth-child(2) > span:nth-child(1) > font')
            if shortname_tag:
                journal['shortname'] = shortname_tag.get_text(strip=True)
            # letpub评分
            letpub_score_tag = tr.select_one('td:nth-child(2) > span:nth-child(2) > span:nth-child(2) > div:nth-child(1)')
            if letpub_score_tag:
                journal['letpub_score'] = letpub_score_tag.get_text(strip=True)
            # letpub打分人数
            score_people_tag = tr.select_one('td:nth-child(2) > span:nth-child(2) > span:nth-child(2) > div:nth-child(3)')
            if score_people_tag:
                journal['score_people'] = score_people_tag.get_text(strip=True).split('人')[0]
            # 声誉分
            reputation_score_tag = tr.select_one('td:nth-child(2) > span:nth-child(2) > div:nth-child(6)')
            if reputation_score_tag:
                journal['reputation_score'] = reputation_score_tag.get_text(strip=True)
            # 影响力分
            influence_score_tag = tr.select_one('td:nth-child(2) > span:nth-child(2) > div:nth-child(10)')
            if influence_score_tag:
                journal['influence_score'] = influence_score_tag.get_text(strip=True)
            # 速度分
            speed_score_tag = tr.select_one('td:nth-child(2) > span:nth-child(2) > div:nth-child(14)')
            if speed_score_tag:
                journal['speed_score'] = speed_score_tag.get_text(strip=True)
        elif '期刊ISSN' in first_cell_text:
            # 期刊ISSN
            ISSN_tag = tr.select_one('td:nth-child(2)')
            if ISSN_tag:
                journal['issn'] = ISSN_tag.get_text(strip=True)
        elif 'P-ISSN' in first_cell_text:
            # P-ISSN
            P_ISSN_tag = tr.select_one('td:nth-child(2)')
            if P_ISSN_tag:
                journal['p_issn'] = P_ISSN_tag.get_text(strip=True)
        elif 'E-ISSN' in first_cell_text:
            # E-ISSN
            E_ISSN_tag = tr.select_one('td:nth-child(2)')
            if E_ISSN_tag:
                journal['e_issn'] = E_ISSN_tag.get_text(strip=True)
        elif '2023-2024最新影响因子' in first_cell_text or '2024-2025最新影响因子' in first_cell_text or '最新影响因子' in first_cell_text:
            # 最新影响因子
            if_tag = tr.select_one('td:nth-child(2)')
            if if_tag:
                journal['impact_factor'] = if_tag.text.split('点击')[0].strip()
        elif '实时影响因子' in first_cell_text:
            # 实时影响因子
            real_time_if_tag = tr.select_one('td:nth-child(2)')
            if real_time_if_tag:
                journal['real_time_if'] = real_time_if_tag.get_text(strip=True).split('：')[-1]
        elif '自引率' in first_cell_text and '趋势图' not in first_cell_text:
            # 自引率
            self_cite_rate_tag = tr.select_one('td:nth-child(2)')
            if self_cite_rate_tag:
                journal['self_cite_rate'] = self_cite_rate_tag.text.split('点击')[0].strip()
        elif '五年影响因子' in first_cell_text:
            # 五年影响因子
            five_year_if_tag = tr.select_one('td:nth-child(2)')
            if five_year_if_tag:
                journal['five_year_if'] = five_year_if_tag.get_text(strip=True)
        elif 'JCI期刊引文指标' in first_cell_text:
            # JCI期刊引文指标
            jci_tag = tr.select_one('td:nth-child(2)')
            if jci_tag:
                journal['jci'] = jci_tag.get_text(strip=True)
        elif 'h-index' in first_cell_text:
            # h-index
            h_index_tag = tr.select_one('td:nth-child(2)')
            if h_index_tag:
                journal['h_index'] = h_index_tag.get_text(strip=True)
        elif 'CiteScore' in first_cell_text:
            tr_tr = tr.select_one('td:nth-child(2) > table > tbody > tr:nth-child(2)')
            if tr_tr:
                cite_score_tag = tr_tr.select_one('td:nth-child(1)')
                if cite_score_tag:
                    journal['cite_score'] = cite_score_tag.get_text(strip=True)

                sjr_tag = tr_tr.select_one('td:nth-child(2)')
                if sjr_tag:
                    journal['sjr'] = sjr_tag.get_text(strip=True)

                snip_tag = tr_tr.select_one('td:nth-child(3)')
                if snip_tag:
                    journal['snip'] = snip_tag.get_text(strip=True)

                tab_tag = tr_tr.select_one('td:nth-child(4) > table')
                if tab_tag:
                    tr_tr_tr = tab_tag.find_all('tr')[1:]
                    rank_list = []
                    for tmp_tr in tr_tr_tr:
                        rank_dict = {'学科': '', '分区': '', '排名': '', '百分位': ''}
                        subject_tag = tmp_tr.select_one('td:nth-child(1)')
                        if subject_tag:
                            subject = subject_tag.get_text(strip=True)
                            if '大类：' in subject and '小类：' in subject:
                                major = subject.split("大类：")[1].split("小类：")[0].strip()
                                minor = subject.split("小类：")[1].strip()
                                rank_dict['学科'] = major + '-' + minor
                            else:
                                rank_dict['学科'] = subject

                        part_tag = tmp_tr.select_one('td:nth-child(2)')
                        if part_tag:
                            rank_dict['分区'] = part_tag.get_text(strip=True)

                        rank_tag = tmp_tr.select_one('td:nth-child(3)')
                        if rank_tag:
                            rank_dict['排名'] = rank_tag.get_text(strip=True)

                        percentage_tag = tmp_tr.select_one('td:nth-child(4)')
                        if percentage_tag:
                            rank_dict['百分位'] = percentage_tag.get_text(strip=True)

                        rank_list.append(rank_dict)
                    journal['cite_score_rank'] = rank_list
        elif '期刊简介' in first_cell_text:
            # 期刊简介
            intro_tag = tr.select_one('#readmore_content')
            if intro_tag:
                journal['intro'] = intro_tag.get_text(strip=True)
        elif '期刊官方网站' in first_cell_text:
            # 期刊官方网站
            website_tag = tr.select_one('td:nth-child(2) > a')
            if website_tag:
                journal['website'] = website_tag.get_text(strip=True)
        elif '期刊投稿格式模板' in first_cell_text:
            # 会员信息，不做处理
            pass
        elif '期刊投稿网址' in first_cell_text:
            # 期刊投稿网址
            submission_url_tag = tr.select_one('td:nth-child(2) > a')
            if submission_url_tag:
                journal['submission_url'] = submission_url_tag.get_text(strip=True)
        elif '作者指南网址' in first_cell_text:
            # 作者指南网址
            guidelines_url_tag = tr.select_one('td:nth-child(2) > a')
            if guidelines_url_tag:
                journal['guidelines_url'] = guidelines_url_tag.get_text(strip=True)
        elif '期刊语言要求' in first_cell_text:
            language_require_tag = tr.select_one('td:nth-child(2)')
            if language_require_tag:
                journal['language_require'] = language_require_tag.get_text(strip=True).split('经LetPub语言')[0].strip()
        elif '是否OA开放访问' in first_cell_text:
            # 是否OA开放访问
            open_access_tag = tr.select_one('td:nth-child(2)')
            if open_access_tag:
                journal['open_access'] = open_access_tag.get_text(strip=True) == 'Yes'
        elif 'OA期刊相关信息' in first_cell_text:
            oa_info_tag = tr.select_one('td:nth-child(2)')
            if oa_info_tag:
                match = re.search(r'USD\s?(\d+)', oa_info_tag.get_text(strip=True))
                journal['oa_price'] = int(match.group(1)) if match else None
        elif '通讯方式' in first_cell_text:
            # 通讯方式
            communication_tag = tr.select_one('td:nth-child(2)')
            if communication_tag:
                journal['communication'] = communication_tag.get_text(strip=True)
        elif '出版商' in first_cell_text:
            # 出版商
            publisher_tag = tr.select_one('td:nth-child(2)')
            if publisher_tag:
                journal['publisher'] = publisher_tag.get_text(strip=True)
        elif '涉及的研究方向' in first_cell_text:
            # 涉及的研究方向
            field_tag = tr.select_one('td:nth-child(2)')
            if field_tag:
                journal['field'] = field_tag.get_text(strip=True)
        elif '出版国家或地区' in first_cell_text:
            # 出版国家或地区
            country_tag = tr.select_one('td:nth-child(2)')
            if country_tag:
                journal['country'] = country_tag.get_text(strip=True)
        elif '出版语言' in first_cell_text:
            # 出版语言
            language_tag = tr.select_one('td:nth-child(2)')
            if language_tag:
                journal['language'] = language_tag.get_text(strip=True)
        elif '出版周期' in first_cell_text:
            # 出版周期
            period_tag = tr.select_one('td:nth-child(2)')
            if period_tag:
                journal['period'] = period_tag.get_text(strip=True)
        elif '出版年份' in first_cell_text:
            # 出版年份
            start_year_tag = tr.select_one('td:nth-child(2)')
            if start_year_tag:
                journal['start_year'] = start_year_tag.get_text(strip=True)
        elif '年文章数' in first_cell_text and '趋势图' not in first_cell_text:
            # 年文章数
            year_paper_tag = tr.select_one('td:nth-child(2)')
            if year_paper_tag:
                journal['year_paper'] = year_paper_tag.text.split('点击')[0].strip()
        elif 'Gold OA文章占比' in first_cell_text:
            # Gold OA文章占比
            gold_oa_tag = tr.select_one('td:nth-child(2)')
            if gold_oa_tag:
                journal['gold_oa'] = gold_oa_tag.get_text(strip=True)
        elif '研究类文章占比' in first_cell_text:
            # 研究类文章占比
            research_ratio_tag = tr.select_one('td:nth-child(2)')
            if research_ratio_tag:
                journal['research_ratio'] = research_ratio_tag.get_text(strip=True)
        elif 'WOS期刊JCR分区' in first_cell_text or 'WOS期刊SCI分区' in first_cell_text:
            sci_part_tag = tr.select_one('td:nth-child(2) > span')
            if sci_part_tag:
                journal['sci_part'] = sci_part_tag.get_text(strip=True)
            if not journal.get('sci_part'):
                td2 = tr.select_one('td:nth-child(2)')
                if td2:
                    text = td2.get_text(strip=True)
                    match = re.search(r'WOS分区等级：(.+?区)', text)
                    if match:
                        journal['sci_part'] = match.group(1)

            tab_tags = tr.find_all('table')
            if tab_tags:
                rank_dict = {'学科': '', '收录子集': '', '分区': '', '排名': '', '百分位': ''}
                for tab_tag in tab_tags:
                    tr_tr = tab_tag.select_one('tbody > tr:nth-child(2)')
                    if tr_tr:
                        subject_tag = tr_tr.select_one('td:nth-child(1)')
                        if subject_tag:
                            rank_dict['学科'] = subject_tag.get_text(strip=True).split('学科：')[1].strip()

                        subset_tag = tr_tr.select_one('td:nth-child(2)')
                        if subset_tag:
                            rank_dict['收录子集'] = subset_tag.get_text(strip=True)

                        part_tag = tr_tr.select_one('td:nth-child(3)')
                        if part_tag:
                            rank_dict['分区'] = part_tag.get_text(strip=True)

                        rank_tag = tr_tr.select_one('td:nth-child(4)')
                        if rank_tag:
                            rank_dict['排名'] = rank_tag.get_text(strip=True)

                        percentage_tag = tr_tr.select_one('td:nth-child(5)')
                        if percentage_tag:
                            rank_dict['百分位'] = percentage_tag.get_text(strip=True)

                        tmp_td_tag = tab_tag.select_one('tbody > tr:nth-child(1) > td:nth-child(1)')
                        if tmp_td_tag:
                            if '按JIF指标学科分区' in tmp_td_tag.get_text(strip=True):
                                journal['jif_sci_rank'] = rank_dict
                            elif '按JCI指标学科分区' in tmp_td_tag.get_text(strip=True):
                                journal['jci_sci_rank'] = rank_dict
        elif '期刊分区表预警名单' in first_cell_text or '中国科学院《国际期刊预警名单（试行）》名单' in first_cell_text:
            # 期刊分区表预警名单
            warning_tag = tr.select_one('td:nth-child(2)')
            if warning_tag:
                pattern = r'\d{4}年\d{2}月发布的[^：]*版[：:](.*?)\s*(?=\d{4}年|\Z)'
                matches = re.findall(pattern, warning_tag.get_text(strip=True))
                journal['warning'] = not all(s.strip() == '不在预警名单中' for s in matches)
        elif '期刊分区表' in first_cell_text and '2025年3月升级版' in first_cell_text:
            # 期刊分区表（2025年3月升级版）
            tab_tags = tr.select_one('table')
            if tab_tags:
                part_dict = {'大类学科': '', '小类学科': '', 'Top期刊': False, '综述期刊': False, '分区': ''}
                data_row = tab_tags.select_one('tr:nth-child(2)')
                if data_row:
                    major_subject_tag = data_row.select_one('td:nth-child(1)')
                    if major_subject_tag:
                        # 提取学科名称（排除分区span）
                        text = major_subject_tag.get_text(strip=True)
                        # 使用正则提取学科名称（在第一个数字之前）
                        match = re.match(r'^([^\d]+)', text)
                        if match:
                            part_dict['大类学科'] = match.group(1).strip()
                        # 提取分区（取第一个可见的分区）
                        part_span = major_subject_tag.select_one('span:not([style*="display:none"])')
                        if part_span:
                            part_dict['分区'] = part_span.get_text(strip=True)

                    minor_subject_tag = data_row.select_one('td:nth-child(2) table')
                    if minor_subject_tag:
                        # 获取嵌套表格第一个 td
                        first_td = minor_subject_tag.select_one('tr td:nth-child(1)')
                        if first_td:
                            # 只取直接文本，排除子元素
                            text = ''.join([c for c in first_td.contents if c.name is None])
                            part_dict['小类学科'] = text.strip()

                    top_tag = data_row.select_one('td:nth-child(3)')
                    if top_tag:
                        part_dict['Top期刊'] = top_tag.get_text(strip=True) == '是'

                    review_tag = data_row.select_one('td:nth-child(4)')
                    if review_tag:
                        part_dict['综述期刊'] = review_tag.get_text(strip=True) == '是'

                journal['ch_sci_2025'] = part_dict
        elif '期刊分区表' in first_cell_text and '2023年12月旧的升级版' in first_cell_text:
            # 期刊分区表（2023年12月升级版）
            tab_tags = tr.select_one('table')
            if tab_tags:
                part_dict = {'大类学科': '', '小类学科': '', 'Top期刊': False, '综述期刊': False, '分区': ''}
                data_row = tab_tags.select_one('tr:nth-child(2)')
                if data_row:
                    major_subject_tag = data_row.select_one('td:nth-child(1)')
                    if major_subject_tag:
                        text = major_subject_tag.get_text(strip=True)
                        match = re.match(r'^([^\d]+)', text)
                        if match:
                            part_dict['大类学科'] = match.group(1).strip()
                        part_span = major_subject_tag.select_one('span:not([style*="display:none"])')
                        if part_span:
                            part_dict['分区'] = part_span.get_text(strip=True)

                    minor_subject_tag = data_row.select_one('td:nth-child(2) table')
                    if minor_subject_tag:
                        # 获取嵌套表格第一个 td
                        first_td = minor_subject_tag.select_one('tr td:nth-child(1)')
                        if first_td:
                            # 只取直接文本，排除子元素
                            text = ''.join([c for c in first_td.contents if c.name is None])
                            part_dict['小类学科'] = text.strip()

                    top_tag = data_row.select_one('td:nth-child(3)')
                    if top_tag:
                        part_dict['Top期刊'] = top_tag.get_text(strip=True) == '是'

                    review_tag = data_row.select_one('td:nth-child(4)')
                    if review_tag:
                        part_dict['综述期刊'] = review_tag.get_text(strip=True) == '是'

                journal['ch_sci_2023'] = part_dict
        elif '期刊分区表' in first_cell_text and '2022年12月旧的升级版' in first_cell_text:
            # 期刊分区表（2022年12月旧的升级版）
            tab_tags = tr.select_one('table')
            if tab_tags:
                part_dict = {'大类学科': '', '小类学科': '', 'Top期刊': False, '综述期刊': False, '分区': ''}
                data_row = tab_tags.select_one('tr:nth-child(2)')
                if data_row:
                    major_subject_tag = data_row.select_one('td:nth-child(1)')
                    if major_subject_tag:
                        text = major_subject_tag.get_text(strip=True)
                        match = re.match(r'^([^\d]+)', text)
                        if match:
                            part_dict['大类学科'] = match.group(1).strip()
                        part_span = major_subject_tag.select_one('span:not([style*="display:none"])')
                        if part_span:
                            part_dict['分区'] = part_span.get_text(strip=True)

                    minor_subject_tag = data_row.select_one('td:nth-child(2) table')
                    if minor_subject_tag:
                        # 获取嵌套表格第一个 td
                        first_td = minor_subject_tag.select_one('tr td:nth-child(1)')
                        if first_td:
                            # 只取直接文本，排除子元素
                            text = ''.join([c for c in first_td.contents if c.name is None])
                            part_dict['小类学科'] = text.strip()

                    top_tag = data_row.select_one('td:nth-child(3)')
                    if top_tag:
                        part_dict['Top期刊'] = top_tag.get_text(strip=True) == '是'

                    review_tag = data_row.select_one('td:nth-child(4)')
                    if review_tag:
                        part_dict['综述期刊'] = review_tag.get_text(strip=True) == '是'

                journal['ch_sci_2022'] = part_dict
        elif '《新锐期刊分区表》' in first_cell_text:
            # 新锐期刊分区表（2026年3月发布）
            tab_tags = tr.select_one('table')
            if tab_tags:
                part_dict = {'大类学科': '', '小类学科': '', 'Top期刊': False, '综述期刊': False, '分区': ''}
                data_row = tab_tags.select_one('tr:nth-child(2)')
                if data_row:
                    major_subject_tag = data_row.select_one('td:nth-child(1)')
                    if major_subject_tag:
                        text = major_subject_tag.get_text(strip=True)
                        match = re.match(r'^([^\d]+)', text)
                        if match:
                            part_dict['大类学科'] = match.group(1).strip()
                        part_span = major_subject_tag.select_one('span:not([style*="display:none"])')
                        if part_span:
                            part_dict['分区'] = part_span.get_text(strip=True)

                    minor_subject_tag = data_row.select_one('td:nth-child(2) table')
                    if minor_subject_tag:
                        # 获取嵌套表格第一个 td
                        first_td = minor_subject_tag.select_one('tr td:nth-child(1)')
                        if first_td:
                            # 只取直接文本，排除子元素
                            text = ''.join([c for c in first_td.contents if c.name is None])
                            part_dict['小类学科'] = text.strip()

                    top_tag = data_row.select_one('td:nth-child(3)')
                    if top_tag:
                        part_dict['Top期刊'] = top_tag.get_text(strip=True) == '是'

                    review_tag = data_row.select_one('td:nth-child(4)')
                    if review_tag:
                        part_dict['综述期刊'] = review_tag.get_text(strip=True) == '是'

                journal['ch_sci_2026'] = part_dict
        elif 'SCI期刊收录coverage' in first_cell_text:
            sci_tag = tr.select_one('td:nth-child(2)')
            if sci_tag:
                text = sci_tag.get_text(strip=True)
                journal['sci'] = 'Science Citation Index Expanded (SCIE)' in text
                journal['scopus'] = 'Scopus (CiteScore)' in text
        elif 'PubMed Central (PMC)链接' in first_cell_text:
            # PubMed Central (PMC)链接
            pmc_url_tag = tr.select_one('td:nth-child(2) > a')
            if pmc_url_tag:
                journal['pmc_url'] = pmc_url_tag.get_text(strip=True)
        elif '平均审稿速度' in first_cell_text:
            # 平均审稿速度
            speed_tag = tr.select_one('td:nth-child(2)')
            if speed_tag:
                text = speed_tag.get_text(strip=True)
                # 在"来源"前加分号
                text = text.replace('来源', '；来源')
                journal['speed'] = text
        elif '平均录用比例' in first_cell_text:
            # 平均录用比例
            accept_tag = tr.select_one('td:nth-child(2)')
            if accept_tag:
                text = accept_tag.get_text(strip=True)
                # 在"来源"前加分号
                text = text.replace('来源', '；来源')
                journal['accept'] = text
        elif 'APC文章处理费信息' in first_cell_text:
            apc_tag = tr.select_one('td:nth-child(2)')
            if apc_tag:
                match = re.search(r'USD\s?(\d+)', apc_tag.get_text(strip=True))
                journal['apc_price'] = int(match.group(1)) if match else None
        elif 'LetPub助力发表' in first_cell_text:
            # 广告，不做处理
            pass
        elif '收稿范围' in first_cell_text:
            range_tag = tr.select_one('td:nth-child(2)')
            if range_tag:
                journal['range'] = range_tag.get_text(strip=True).split('数据：')[1]
        elif '收录体裁' in first_cell_text:
            type_tag = tr.select_one('td:nth-child(2)')
            if type_tag:
                journal['type'] = type_tag.get_text(strip=True).split('数据：')[1]
        elif '编辑信息' in first_cell_text:
            editor_tag = tr.select_one('td:nth-child(2)')
            if editor_tag:
                journal['editor'] = editor_tag.get_text(strip=True)
        elif '期刊常用信息链接' in first_cell_text:
            # 无关信息，不做处理
            pass

    # 额外处理：在所有 table.table_yjfx 的 td 中查找嵌套的表格
    nested_tables = []
    if yxyz_content:
        for table in yxyz_content.select('table.table_yjfx'):
            nested_tables.extend(table.find_all('table'))
    for nested_table in nested_tables:
        # 检查是否是 JCI 分区表格
        header_row = nested_table.select_one('tr:nth-child(1)')
        if header_row:
            header_text = header_row.get_text(strip=True)
            if '按JCI指标学科分区' in header_text:
                data_row = nested_table.select_one('tr:nth-child(2)')
                if data_row:
                    rank_dict = {'学科': '', '收录子集': '', '分区': '', '排名': '', '百分位': ''}
                    subject_tag = data_row.select_one('td:nth-child(1)')
                    if subject_tag:
                        rank_dict['学科'] = subject_tag.get_text(strip=True).split('学科：')[1].strip() if '学科：' in subject_tag.get_text(strip=True) else subject_tag.get_text(strip=True)

                    subset_tag = data_row.select_one('td:nth-child(2)')
                    if subset_tag:
                        rank_dict['收录子集'] = subset_tag.get_text(strip=True)

                    part_tag = data_row.select_one('td:nth-child(3)')
                    if part_tag:
                        rank_dict['分区'] = part_tag.get_text(strip=True)

                    rank_tag = data_row.select_one('td:nth-child(4)')
                    if rank_tag:
                        rank_dict['排名'] = rank_tag.get_text(strip=True)

                    percentage_tag = data_row.select_one('td:nth-child(5)')
                    if percentage_tag:
                        rank_dict['百分位'] = percentage_tag.get_text(strip=True)

                    journal['jci_sci_rank'] = rank_dict
            elif '按JIF指标学科分区' in header_text:
                data_row = nested_table.select_one('tr:nth-child(2)')
                if data_row:
                    rank_dict = {'学科': '', '收录子集': '', '分区': '', '排名': '', '百分位': ''}
                    subject_tag = data_row.select_one('td:nth-child(1)')
                    if subject_tag:
                        rank_dict['学科'] = subject_tag.get_text(strip=True).split('学科：')[1].strip() if '学科：' in subject_tag.get_text(strip=True) else subject_tag.get_text(strip=True)

                    subset_tag = data_row.select_one('td:nth-child(2)')
                    if subset_tag:
                        rank_dict['收录子集'] = subset_tag.get_text(strip=True)

                    part_tag = data_row.select_one('td:nth-child(3)')
                    if part_tag:
                        rank_dict['分区'] = part_tag.get_text(strip=True)

                    rank_tag = data_row.select_one('td:nth-child(4)')
                    if rank_tag:
                        rank_dict['排名'] = rank_tag.get_text(strip=True)

                    percentage_tag = data_row.select_one('td:nth-child(5)')
                    if percentage_tag:
                        rank_dict['百分位'] = percentage_tag.get_text(strip=True)

                    journal['jif_sci_rank'] = rank_dict

    # 提取同类著名期刊
    similar_journals = []
    similar_table = soup.find('th', string='同类著名期刊名称')
    if similar_table:
        table = similar_table.find_parent('table')
        if table:
            rows = table.find_all('tr')[1:]  # 跳过表头
            for row in rows:
                tds = row.find_all('td')
                if len(tds) >= 3:
                    journal_info = {}
                    # 期刊名称和链接
                    name_link = tds[0].select_one('a')
                    if name_link:
                        journal_info['name'] = name_link.get_text(strip=True)
                        href = name_link.get('href', '')
                        if 'journalid=' in href:
                            journal_info['journal_id'] = href.split('journalid=')[-1].split('&')[0]
                    # h-index
                    journal_info['h_index'] = tds[1].get_text(strip=True)
                    # CiteScore
                    journal_info['cite_score'] = tds[2].get_text(strip=True)
                    if journal_info:
                        similar_journals.append(journal_info)
    if similar_journals:
        journal['similar_journals'] = similar_journals

    return journal


if __name__ == "__main__":
    import requests
    import json
    
    # 测试解析期刊详情
    url = "https://letpub.com.cn/index.php?journalid=1642&page=journalapp&view=detail"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    html_content = response.text
    
    result = parse_journal_detail(html_content)
    print(json.dumps(result, indent=2, ensure_ascii=False))
