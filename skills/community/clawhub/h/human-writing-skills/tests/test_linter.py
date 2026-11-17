import json
import unittest

from humanwriting.linter import format_lint_report, lint_text


class LinterTests(unittest.TestCase):
    def test_reports_evidence_location_and_transparent_score(self):
        report = lint_text(
            "普通开头。\n命运的齿轮开始转动，空气仿佛凝固。",
            style="fiction",
        )
        rule_ids = {finding.rule_id for finding in report.findings}
        self.assertIn("LEX002", rule_ids)
        self.assertIn("ATM001", rule_ids)
        fate = next(finding for finding in report.findings if finding.rule_id == "LEX002")
        self.assertEqual((fate.line, fate.column), (2, 1))
        self.assertGreater(report.score, 0)
        self.assertIn("not evidence of AI authorship", report.disclaimer)

    def test_masks_code_blocks_block_quotes_and_urls(self):
        report = lint_text(
            "```text\n命运的齿轮开始转动\n```\n"
            "> 空气仿佛凝固\n"
            "https://example.com/delve\n"
            "正文很平静。",
            style="fiction",
        )
        self.assertEqual(report.findings, ())

    def test_allowlist_suppresses_rule_or_category(self):
        by_rule = lint_text("命运的齿轮开始转动。", style="fiction", allow={"LEX002"})
        by_category = lint_text(
            "命运的齿轮开始转动。",
            style="fiction",
            allow={"inflated-vocabulary"},
        )
        self.assertEqual(by_rule.findings, ())
        self.assertEqual(by_category.findings, ())

    def test_false_precision_is_genre_aware(self):
        fiction = lint_text("她的手向上移动了三厘米。", style="fiction")
        academic = lint_text("伤口长度为三厘米。", style="academic-paper")
        forensic_fiction = lint_text("法医鉴定报告写明，伤口长2.3厘米。", style="fiction")
        self.assertIn("PREC001", {finding.rule_id for finding in fiction.findings})
        self.assertNotIn("PREC001", {finding.rule_id for finding in academic.findings})
        self.assertNotIn("PREC001", {finding.rule_id for finding in forensic_fiction.findings})

    def test_reports_bidirectional_contrast_and_comparison_ladder(self):
        text = (
            "这不是谨慎，是拖延。那是拒绝，不是犹豫。"
            "走廊比昨夜更窄，比她记忆里更长。"
        )
        report = lint_text(text, style="fiction")
        rule_ids = {finding.rule_id for finding in report.findings}
        self.assertIn("STR001", rule_ids)
        self.assertIn("STR002", rule_ids)

    def test_reports_repeated_contrast_density(self):
        text = "这不是谨慎，是拖延。那是拒绝，不是犹豫。他不是镇定，而是麻木。"
        report = lint_text(text, style="fiction")
        self.assertIn("STR003", {finding.rule_id for finding in report.findings})

    def test_three_comparisons_escalate_and_two_remain_reviewable(self):
        two = lint_text("风比刚才冷，比走廊里更硬。", style="fiction")
        three = lint_text("风比刚才冷，比走廊硬，比她记忆里的冬天更长。", style="fiction")
        self.assertIn("STR002", {finding.rule_id for finding in two.findings})
        self.assertNotIn("STR004", {finding.rule_id for finding in two.findings})
        severe = next(finding for finding in three.findings if finding.rule_id == "STR004")
        self.assertEqual(severe.severity, "high")

    def test_comparison_ladder_respects_serious_style_and_nonmarkers(self):
        serious = lint_text("实验组比对照组高，比基线低。", style="academic-paper")
        nonmarkers = lint_text("同比和环比数据用于比较比例。", style="fiction")
        self.assertNotIn("STR002", {finding.rule_id for finding in serious.findings})
        self.assertNotIn("STR002", {finding.rule_id for finding in nonmarkers.findings})

    def test_reports_high_confidence_omission_symptom(self):
        report = lint_text("他刚想把。她原本打算从。", style="fiction")
        omissions = [finding for finding in report.findings if finding.rule_id == "SYN001"]
        self.assertEqual(len(omissions), 2)
        allowed = lint_text("他刚想把。", style="fiction", allow={"possible-omission"})
        self.assertNotIn("SYN001", {finding.rule_id for finding in allowed.findings})

    def test_reports_extended_surface_pattern_families(self):
        text = (
            "有专家认为，这标志着一个关键时刻。"
            "尽管项目面临很多挑战，它仍然继续向前发展。"
            "本书从星系到药物，从记忆到桥梁。"
        )
        rule_ids = {finding.rule_id for finding in lint_text(text).findings}
        self.assertTrue({"ATTR001", "SIGN001", "CHALLENGE001", "RANGE001"} <= rule_ids)

    def test_reports_density_without_banning_single_words_or_formats(self):
        clustered = lint_text("赋能产业，助力增长，深耕市场，开启新篇章。")
        single = lint_text("这项工具可以助力校对。")
        formatted = lint_text(
            "- **目标：** 完成审核\n- **范围：** 两章\n- **结果：** 修改三处\n"
            "## Product Strategy Review\n## Market Risk Analysis\n## Customer Value Report\n"
        )
        self.assertIn("LEX003", {finding.rule_id for finding in clustered.findings})
        self.assertNotIn("LEX003", {finding.rule_id for finding in single.findings})
        self.assertTrue(
            {"FORMAT001", "FORMAT003"}
            <= {finding.rule_id for finding in formatted.findings}
        )

    def test_reports_narrative_synonym_cycling_only_for_narrative_styles(self):
        text = "主人公推门。主角停了一下。中心人物最后走进雨里。"
        fiction = lint_text(text, style="fiction")
        news = lint_text(text, style="news-report")
        self.assertIn("ALIAS001", {finding.rule_id for finding in fiction.findings})
        self.assertNotIn("ALIAS001", {finding.rule_id for finding in news.findings})

    def test_narrative_mini_headings_and_multilingual_time_cards_are_flagged(self):
        samples = (
            "上午她一直守着电话。\n\n## 下午\n\n门终于响了。",
            "He kept the receipt.\n\n### The confrontation\n\nShe opened the door.",
            "朝は雨だった。\n\n午後\n\n彼女は駅を出た。",
            "Il attendit sans répondre.\n\nL’après-midi\n\nLa porte s’ouvrit.",
            "Ella guardó la carta.\n\nPor la tarde\n\nVolvió a la estación.",
            "Ela não largou a chave.\n\nÀ noite\n\nA campainha tocou.",
            "احتفظت بالرسالة.\n\nفي المساء\n\nفُتح الباب.",
            "Epistulam servavit.\n\nVespere\n\nIanua aperta est.",
        )
        for text in samples:
            with self.subTest(text=text):
                rule_ids = {item.rule_id for item in lint_text(text, style="fiction").findings}
                self.assertTrue({"HEAD001", "HEAD002"} & rule_ids)

    def test_narrative_heading_rules_preserve_titles_chapters_and_serious_sections(self):
        titled_fiction = lint_text(
            "# The Long Road\n\n## Chapter 1 Arrival\n\nShe missed the train.",
            style="fiction",
        )
        news = lint_text(
            "## Afternoon update\n\nThe agency released the revised count.",
            style="news-report",
        )
        natural_bridge = lint_text(
            "她把上午没写完的地址压在杯底。到下午雨停时，墨迹已经洇成一团。",
            style="fiction",
        )
        self.assertFalse({"HEAD001", "HEAD002"} & {item.rule_id for item in titled_fiction.findings})
        self.assertFalse({"HEAD001", "HEAD002"} & {item.rule_id for item in news.findings})
        self.assertFalse({"HEAD001", "HEAD002"} & {item.rule_id for item in natural_bridge.findings})
        for chapter in (
            "## 第二章 雨停以后",
            "## 第三話 帰還",
            "## Chapitre premier Le retour",
            "## Capítulo uno El regreso",
            "## Capítulo um O retorno",
            "## Capitulum primum Reditus",
            "## الفصل الأول العودة",
        ):
            with self.subTest(chapter=chapter):
                report = lint_text(f"# Book\n\n{chapter}\n\nText.", style="fiction")
                self.assertFalse({"HEAD001", "HEAD002"} & {item.rule_id for item in report.findings})

    def test_narrative_heading_rules_are_allowlisted(self):
        report = lint_text(
            "上午没有回信。\n\n下午\n\n门铃响了。",
            style="fiction",
            allow={"narrative-time-card"},
        )
        self.assertNotIn("HEAD002", {item.rule_id for item in report.findings})

    def test_json_output_contains_structured_spans(self):
        report = lint_text("In today's fast-paced world, let's dive in.")
        payload = json.loads(format_lint_report(report, "json"))
        self.assertIn("score", payload)
        self.assertIn("findings", payload)
        self.assertIn("start", payload["findings"][0])
        self.assertIn("line", payload["findings"][0])

    def test_reports_dense_imagery_fragment_runs_and_detail_inventory(self):
        text = (
            "他三十八岁，身高一米八，体重七十五公斤，职业是律师。\n\n"
            "雨像旧胶片，灯仿佛一只眼，门如同一张嘴，风宛如叹息。\n\n"
            "深圳。\n\n酒店。\n\n深夜。\n\n电话响了。"
        )
        report = lint_text(text, style="fiction")
        rule_ids = {finding.rule_id for finding in report.findings}
        self.assertTrue({"INFO001", "IMG001", "PARA001"} <= rule_ids)

    def test_new_texture_rules_do_not_run_for_serious_styles(self):
        text = "患者三十八岁，身高一米八，体重七十五公斤，职业是律师。"
        report = lint_text(text, style="academic-paper")
        self.assertFalse({"INFO001", "IMG001", "PARA001"} & {item.rule_id for item in report.findings})

    def test_allowlist_suppresses_structural_texture_rules(self):
        text = "雨像旧胶片，灯仿佛一只眼，门如同一张嘴，风宛如叹息。"
        by_rule = lint_text(text, style="fiction", allow={"IMG001"})
        by_category = lint_text(text, style="fiction", allow={"imagery-density"})
        self.assertNotIn("IMG001", {item.rule_id for item in by_rule.findings})
        self.assertNotIn("IMG001", {item.rule_id for item in by_category.findings})

    def test_reports_cinematic_opening_and_repeated_vague_introspection(self):
        text = (
            "第一章 抵达\n\n"
            "傍晚六点半，临港机场二号航站楼，落日照着玻璃。她身穿深色制服，"
            "心里莫名有一股说不清的感觉。\n\n"
            "她不知道为什么没有回信。后来又莫名地笑了一下。"
        )
        report = lint_text(text, style="webnovel")
        rule_ids = {item.rule_id for item in report.findings}
        self.assertTrue({"OPEN002", "EMO003"} <= rule_ids)

    def test_reports_repeated_scenic_chapter_resets(self):
        text = (
            "第一章 到站\n\n清晨，临港车站下着雨。她穿着灰色外套，走进大厅。\n\n"
            "第二章 见面\n\n傍晚，滨江酒店亮起灯光。她换上黑色西装，走向前台。\n\n"
            "第三章 离开\n\n夜里，城南码头吹着冷风。她穿着长裙，站在路口。"
        )
        report = lint_text(text, style="webnovel")
        self.assertIn("RESET001", {item.rule_id for item in report.findings})

    def test_new_scene_rules_are_narrative_only_and_allowlisted(self):
        text = (
            "傍晚六点半，临港机场二号航站楼，落日照着玻璃。"
            "她身穿深色制服，心里莫名有一股说不清的感觉。"
        )
        serious = lint_text(text, style="news-report")
        allowed = lint_text(text, style="fiction", allow={"cinematic-opening-stack"})
        self.assertNotIn("OPEN002", {item.rule_id for item in serious.findings})
        self.assertNotIn("OPEN002", {item.rule_id for item in allowed.findings})

    def test_reports_repeated_narrative_recipe_and_abstract_closures(self):
        text = (
            "清晨，江边的雾贴着路灯。她穿着灰外套，心里莫名有某种感觉。\n\n"
            "上午，车站的雨打在玻璃上。他穿着黑衣，似乎有说不清的情绪。\n\n"
            "傍晚，酒店的灯光落在门口。她穿着长裙，仿佛那点感觉又回来了。\n\n"
            "夜里，码头的冷风吹过来。他穿着旧夹克，莫名觉得一丝不安。\n\n"
            "清晨，医院的灯光亮着。她穿着白衫，似乎有某种感觉。\n\n"
            "后来，窗外的雨停了，仿佛一切都没有发生。"
        )
        rule_ids = {item.rule_id for item in lint_text(text, style="fiction").findings}
        self.assertTrue({"NAT001", "NAT002", "NAT003"} <= rule_ids)

    def test_reports_chinese_reflective_bookend_after_earned_action(self):
        text = (
            "燕子没说话，只是把我搂得更紧了些。"
            "窗外的钱塘，车水马龙，日头一寸一寸地西移。"
            "我们谁也没动——像是要把这一晚错过的，都在这一个下午，慢慢地、安静地，补回来。"
        )
        report = lint_text(text, style="fiction")
        finding = next(item for item in report.findings if item.rule_id == "END001")
        self.assertEqual(finding.category, "reflective-bookend")
        self.assertIn("补回来", finding.excerpt)

    def test_reports_english_stock_reflection_at_story_end(self):
        text = (
            "Mara closed the ledger and returned the key. "
            "At the window, she couldn't help but reflect on what life was and what the future held."
        )
        report = lint_text(text, style="fiction")
        self.assertIn("END001", {item.rule_id for item in report.findings})

    def test_reports_new_argument_and_false_finality_patterns_conservatively(self):
        argumentative = (
            "这是一柄双刃剑。双刃剑会影响不同群体。"
            "不仅如此，更重要的是，毋庸置疑的是，进一步说，证据仍需展开。"
        )
        rules = {item.rule_id for item in lint_text(argumentative, style="argumentative").findings}
        self.assertTrue({"ARG001", "ARG002"} <= rules)
        single = lint_text("这项政策像一柄双刃剑，但报告列出了具体利弊。", style="argumentative")
        self.assertNotIn("ARG001", {item.rule_id for item in single.findings})
        ending = lint_text("她把钥匙交还给他。可是这已经不再重要了。", style="fiction")
        self.assertIn("END002", {item.rule_id for item in ending.findings})
        serious = lint_text("报告称，这已经不再重要了。", style="news-report")
        self.assertNotIn("END002", {item.rule_id for item in serious.findings})

    def test_preserves_quiet_ending_that_changes_material_state(self):
        text = "燕子没说话，只把门卡塞进我掌心。"
        report = lint_text(text, style="fiction")
        self.assertNotIn("END001", {item.rule_id for item in report.findings})

    def test_reflective_bookend_rule_is_narrative_only_and_allowlisted(self):
        text = (
            "窗外的灯一点一点亮起。我们谁也没说话，仿佛这一刻预示着新的开始。"
        )
        serious = lint_text(text, style="news-report")
        allowed = lint_text(text, style="fiction", allow={"reflective-bookend"})
        self.assertNotIn("END001", {item.rule_id for item in serious.findings})
        self.assertNotIn("END001", {item.rule_id for item in allowed.findings})

    def test_checks_terminal_paragraph_before_next_chapter(self):
        text = (
            "第一章 重逢\n\n她把钥匙还给了他。\n\n"
            "窗外暮色渐渐沉下。她不禁思考人生与未来。\n\n"
            "第二章 清晨\n\n电话在六点响了。"
        )
        report = lint_text(text, style="webnovel")
        self.assertIn("END001", {item.rule_id for item in report.findings})

    def test_concrete_quantifier_nouns_do_not_count_as_vague_affect(self):
        text = (
            "一丝阳光落在桌面，一股风从窗缝钻进来，那点零钱压在书下。"
            "这点面粉还够用，一丝灰尘粘在镜面，一股烟从楼道飘过。"
        )
        rule_ids = {item.rule_id for item in lint_text(text, style="fiction").findings}
        self.assertNotIn("NAT002", rule_ids)
        self.assertNotIn("NAT003", rule_ids)

    def test_reports_clustered_dialogue_without_forcing_small_talk_replies(self):
        text = (
            "\“你为什么不告诉我？\”\n\n"
            "窗外的雨落在玻璃上。\n\n"
            "\“你必须回答。\”\n\n"
            "远处的灯一盏盏亮起来。"
        )
        report = lint_text(text, style="fiction")
        self.assertIn("NAT004", {item.rule_id for item in report.findings})

    def test_adjacent_verbal_dialogue_turn_counts_as_a_response(self):
        text = (
            "\u201c你为什么离开？\u201d\n\n"
            "\u201c因为我害怕。\u201d\n\n"
            "\u201c你必须回答。\u201d\n\n"
            "\u201c我已经回答了。\u201d"
        )
        report = lint_text(text, style="fiction")
        self.assertNotIn("NAT004", {item.rule_id for item in report.findings})

    def test_narrative_naturalness_rules_do_not_run_for_serious_styles(self):
        text = (
            "清晨，实验室的灯光亮着。研究员穿着白大褂，似乎有某种感觉。\n\n"
            "上午，医院的雨声持续。患者穿着病服，莫名感到不安。"
        )
        report = lint_text(text, style="academic-paper")
        self.assertFalse(
            {"NAT001", "NAT002", "NAT003", "NAT004"}
            & {item.rule_id for item in report.findings}
        )

    def test_narrative_naturalness_rules_are_allowlisted(self):
        text = (
            "清晨，江边的雾贴着路灯。她穿着灰外套，心里莫名有某种感觉。\n\n"
            "上午，车站的雨打在玻璃上。他穿着黑衣，似乎有说不清的情绪。\n\n"
            "傍晚，酒店的灯光落在门口。她穿着长裙，仿佛那点感觉又回来了。\n\n"
            "夜里，码头的冷风吹过来。他穿着旧夹克，莫名觉得一丝不安。\n\n"
            "清晨，医院的灯光亮着。她穿着白衫，似乎有某种感觉。"
        )
        report = lint_text(
            text,
            style="fiction",
            allow={"narrative-naturalness", "repeated-scene-recipe", "vague-affect-recurrence"},
        )
        rule_ids = {item.rule_id for item in report.findings}
        self.assertNotIn("NAT001", rule_ids)
        self.assertNotIn("NAT002", rule_ids)

    def test_reports_exact_sentence_echo_after_the_scene_has_moved(self):
        repeated = "她把那张车票塞回口袋，决定先不去问站长。"
        text = (
            f"{repeated}\n\n"
            "门外的广播换了班次，她把伞收起来，沿着走廊往售票处走。\n\n"
            f"{repeated}"
        )
        report = lint_text(text, style="fiction")
        self.assertIn("REP001", {item.rule_id for item in report.findings})

    def test_reports_repeated_interpretation_and_action_choreography(self):
        interpretive = "\n\n".join(
            (
                "她看着那只空杯，知道对方已经不想再谈了。",
                "他把文件推回来，她明白这不是商量。",
                "门锁响了一声，她意识到自己没有退路。",
                "电话断线后，她心里清楚这件事不能拖。",
            )
        )
        choreography = "\n\n".join(
            (
                "她一边翻找钥匙，一边听楼道里的脚步声。",
                "他一边整理证据，又一边盯着门缝。",
                "她一边把信折好，一边等电梯停下。",
                "他一边擦掉桌上的水，又一边看向窗外。",
                "她一边把外套搭在椅背上，一边关掉录音。",
            )
        )
        rule_ids = {item.rule_id for item in lint_text(interpretive + "\n\n" + choreography, style="fiction").findings}
        self.assertTrue({"NAT005", "NAT006"} <= rule_ids)

    def test_repetition_findings_are_narrative_only_and_allowlisted(self):
        text = (
            "她知道对方已经不想再谈了。\n\n"
            "她明白这不是商量。\n\n"
            "她意识到自己没有退路。\n\n"
            "她心里清楚这件事不能拖。"
        )
        serious = lint_text(text, style="news-report")
        allowed = lint_text(text, style="fiction", allow={"interpretive-narration-recurrence"})
        self.assertNotIn("NAT005", {item.rule_id for item in serious.findings})
        self.assertNotIn("NAT005", {item.rule_id for item in allowed.findings})

    def test_reports_new_ai_style_patterns_and_genre_boundaries(self):
        cot_text = "究其原因，深层逻辑在于供需关系的失衡。如果深入探究不难发现，归根结底是一场制度博弈。"
        cot_report = lint_text(cot_text, style="argumentative")
        self.assertIn("COT001", {f.rule_id for f in cot_report.findings})

        body_text = "众人倒吸一口凉气，他的瞳孔骤然紧缩，嘴角勾起一抹玩味的冷笑。"
        body_fiction = lint_text(body_text, style="fiction")
        body_paper = lint_text(body_text, style="academic-paper")
        self.assertIn("BODY002", {f.rule_id for f in body_fiction.findings})
        self.assertNotIn("BODY002", {f.rule_id for f in body_paper.findings})

        pseudo_text = "这构成了最真实的底色，为时代写下了最好的注脚，在时间的褶皱里激起微弱的回响。"
        pseudo_report = lint_text(pseudo_text, style="fiction")
        self.assertIn("PSEUDO001", {f.rule_id for f in pseudo_report.findings})

        media_text = "谁懂啊家人们，真的狠狠共情了，治愈内耗直接封神，闭眼入绝绝子！"
        media_report = lint_text(media_text, style="self-media")
        media_news = lint_text(media_text, style="news-report")
        self.assertIn("MEDIA001", {f.rule_id for f in media_report.findings})
        self.assertNotIn("MEDIA001", {f.rule_id for f in media_news.findings})

        slop_text = "This serves as a beacon of innovation to foster and unleash a nuanced ecosystem, bolstered by data."
        slop_report = lint_text(slop_text, style="argumentative")
        self.assertIn("LEX001", {f.rule_id for f in slop_report.findings})


if __name__ == "__main__":
    unittest.main()
