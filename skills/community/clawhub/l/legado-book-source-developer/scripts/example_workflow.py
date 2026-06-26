#!/usr/bin/env python3
"""
Legado Book Source Developer Skill - 工作流示例

这个脚本演示了如何使用 skill 的核心工具来完成书源开发任务。
"""

# ============================================
# 示例1: 标准书源创建工作流
# ============================================

def example_create_book_source():
    """
    完整的书源创建工作流程示例

    这个示例展示了从零开始创建书源的完整过程，
    遵循三阶段工作流程：
    1. 收集信息
    2. 严格审查
    3. 创建书源
    """

    # ==================== 第一阶段：收集信息 ====================

    # 步骤1: 查询知识库
    print("步骤1: 查询知识库")
    print("  - search_knowledge('CSS选择器格式 提取类型 @text @html @ownText @textNode @href @src')")
    print("  - get_css_selector_rules()")
    print("  - get_real_book_source_examples()")
    print("  - get_book_source_templates()")
    print()

    # 步骤2: 检测网站编码
    print("步骤2: 检测网站编码")
    print("  - detect_charset(url='https://example.com')")
    print("  - 记录检测结果: UTF-8 或 GBK")
    print()

    # 步骤3: 获取真实HTML
    print("步骤3: 获取真实HTML")
    print("  - smart_fetch_html(url='https://example.com/search', charset='utf-8')")
    print("  - 分析HTML结构")
    print("  - 识别书籍列表、书名、作者、封面等元素")
    print()

    # ==================== 第二阶段：严格审查 ====================

    # 步骤4: 编写规则
    print("步骤4: 编写规则")
    print("  - 基于知识库规则")
    print("  - 参考真实模板")
    print("  - 使用检测到的编码")
    print("  - 处理特殊情况（无封面、懒加载、信息合并）")
    print()

    # 步骤5: 验证语法
    print("步骤5: 验证语法")
    print("  - CSS选择器格式: CSS选择器@提取类型")
    print("  - 提取类型: @text, @html, @ownText, @textNode, @href, @src")
    print("  - 正则表达式: ##正则表达式##替换内容")
    print("  - JSON结构完整性")
    print()

    # ==================== 第三阶段：创建书源 ====================

    # 步骤6: 生成JSON
    print("步骤6: 生成完整书源JSON")
    print("  - 包含所有必需字段")
    print("  - 应用编写的规则")
    print("  - 处理特殊情况")
    print("  - 参考真实模板格式")
    print()

    # 步骤7: 创建书源
    print("步骤7: 调用 edit_book_source")
    print("  - edit_book_source(complete_source='完整JSON')")
    print("  - 只调用一次")
    print("  - 使用 complete_source 参数")
    print()

    # 步骤8: 输出结果
    print("步骤8: 输出标准JSON数组")
    print("  - 直接复制导入Legado APP")
    print()


# ============================================
# 示例2: CSS选择器使用
# ============================================

def example_css_selectors():
    """
    CSS选择器使用示例

    展示常见的CSS选择器及其在Legado中的应用
    """

    examples = {
        # 元素选择器
        "div@text": "提取div元素及其子元素的文本",
        "a@href": "提取a元素的href属性",
        "img@src": "提取img元素的src属性",

        # 类选择器
        ".title@text": "提取class为title的元素的文本",
        ".author@text": "提取class为author的元素的文本",

        # ID选择器
        "#content@html": "提取id为content的元素的完整HTML",

        # 后代选择器
        ".book-list .item .title@text": "提取嵌套元素的文本",

        # 数字索引（推荐）
        ".item.0@text": "提取第一个item元素",
        ".item.-1@text": "提取倒数第一个item元素",
        ".author.0@text": "提取第一个author元素",
        ".author.1@text": "提取第二个author元素",

        # 文本选择器（替代:contains()）
        "text.下一章@href": "提取包含'下一章'文本的元素的href",

        # 属性选择器
        "[href]@href": "提取有href属性的元素的href",
        "[data-original]@data-original": "提取data-original属性",
    }

    print("CSS选择器示例：")
    for selector, description in examples.items():
        print(f"  {selector:40s} → {description}")
    print()


# ============================================
# 示例3: 正则表达式使用
# ============================================

def example_regex_patterns():
    """
    正则表达式使用示例

    展示在Legado书源规则中如何使用正则表达式
    """

    examples = {
        # 删除前缀
        "##^作者：": "删除开头的'作者：'",
        "##^《": "删除开头的'《'",
        "##^[^|]*\\|": "删除第一个'|'及其前面的内容",

        # 删除后缀
        "##（.*）$": "删除括号及其内容",
        "##》$": "删除结尾的'》'",

        # 提取特定内容
        "##.*作者：(.*)##$1": "提取'作者：'后面的内容",
        "##第(\\d+)章##$1": "提取章节号",
        "##(\\d{4})-(\\d{2})-(\\d{2})##$1年$2月$3日": "格式化日期",

        # 清理广告
        "##<div id=\"ad\">[\\s\\S]*?</div>": "删除广告div",
        "##请收藏本站|本章完|继续阅读": "删除常见提示文本",
        "##免费小说就上.*": "删除网站推广文本",

        # 多个规则
        "##规则1|规则2|规则3##": "使用|分隔多个规则",
    }

    print("正则表达式示例：")
    for pattern, description in examples.items():
        print(f"  {pattern:50s} → {description}")
    print()


# ============================================
# 示例4: 书源模板使用
# ============================================

def example_book_source_templates():
    """
    书源模板使用示例

    展示不同类型网站的模板选择
    """

    templates = {
        "标准小说站": {
            "特征": "有封面、完整信息、独立标签",
            "模板": "Template 1",
            "规则": "完整的搜索、书籍信息、目录、正文规则"
        },
        "笔趣阁类": {
            "特征": "无封面、信息合并、需要正则拆分",
            "模板": "Template 2",
            "规则": "coverUrl留空，使用数字索引和正则表达式"
        },
        "POST请求GBK": {
            "特征": "需要POST请求、GBK编码",
            "模板": "Template 3",
            "规则": "配置method、body、charset参数"
        },
        "懒加载图片": {
            "特征": "图片使用data-original属性",
            "模板": "Template 4",
            "规则": "img@data-original||img@src，添加Referer请求头"
        },
        "分页目录": {
            "特征": "目录有多页，需要分页",
            "模板": "Template 5",
            "规则": "配置nextTocUrl和nextContentUrl"
        },
        "API聚合源": {
            "特征": "返回JSON数据",
            "模板": "Template 6",
            "规则": "使用JSONPath提取数据"
        },
        "动态加载": {
            "特征": "内容需要JavaScript渲染",
            "模板": "Template 7",
            "规则": "添加webView参数和webJs"
        },
        "漫画站": {
            "特征": "图片章节",
            "模板": "Template 8",
            "规则": "bookSourceType: 2，提取所有图片URL"
        },
    }

    print("书源模板使用：")
    for site_type, info in templates.items():
        print(f"\n{site_type}:")
        print(f"  特征: {info['特征']}")
        print(f"  模板: {info['模板']}")
        print(f"  规则: {info['规则']}")
    print()


# ============================================
# 示例5: 编码检测和处理
# ============================================

def example_encoding_detection():
    """
    编码检测和处理示例

    展示如何检测和处理网站编码
    """

    print("编码检测和处理：")
    print()

    # 检测编码
    print("1. 检测网站编码：")
    print("   detected_charset = detect_charset(url='http://example.com')")
    print("   结果: 'utf-8' 或 'gbk'")
    print()

    # UTF-8处理
    print("2. UTF-8编码网站（默认）：")
    utf8_example = """
    searchUrl = "/search?q={{key}}"
    # 或
    searchUrl = "/search?q={{key}},{\"charset\":\"utf-8\"}"
    """
    print(utf8_example)

    # GBK处理
    print("3. GBK编码网站：")
    gbk_example = """
    # GET请求
    searchUrl = "/search?keyword={{key}},{\"charset\":\"gbk\"}"

    # POST请求
    searchUrl = "/search,{\"method\":\"POST\",\"body\":\"key={{key}}\",\"charset\":\"gbk\"}"
    """
    print(gbk_example)

    # 重要原则
    print("4. 重要原则：")
    principles = [
        "编码只需要检测一次",
        "在流程开始时检测",
        "后续所有操作都使用这个编码",
        "避免重复检测",
        "记录检测结果"
    ]
    for principle in principles:
        print(f"   - {principle}")
    print()


# ============================================
# 示例6: nextContentUrl判断
# ============================================

def example_next_content_url():
    """
    nextContentUrl判断示例

    展示如何正确判断是否设置nextContentUrl
    """

    print("nextContentUrl判断规则：")
    print()

    scenarios = {
        "场景1: 真正的下一章（必须设置）": {
            "特征": "按钮链接到真正的下一章节（第一章→第二章）",
            "按钮文字": "下一章、下章、下一节、下一话",
            "URL模式": "/chapter/1.html → /chapter/2.html（章节号变化）",
            "规则": '"nextContentUrl": "text.下一章@href"'
        },
        "场景2: 同一章节分页（必须留空）": {
            "特征": "按钮只是同一章节的分页",
            "按钮文字": "下一页、继续阅读、翻到下一页",
            "URL模式": "/chapter/1_1.html → /chapter/1_2.html（页码变化）",
            "规则": '"nextContentUrl": ""'
        },
        "场景3: 模糊按钮（需要URL判断）": {
            "特征": "按钮文字不明确",
            "按钮文字": "下一、下页",
            "判断方法": "对比当前URL和按钮URL",
            "规则": "章节号变化→设置，页码变化→留空"
        },
    }

    for scenario, info in scenarios.items():
        print(f"{scenario}:")
        print(f"  特征: {info['特征']}")
        print(f"  按钮文字: {info['按钮文字']}")
        print(f"  URL模式: {info['URL模式']}")
        print(f"  规则: {info['规则']}")
        print()

    # 记忆口诀
    print("记忆口诀：")
    mnemonics = [
        "章节号变，设置它",
        "页码变多，留空它",
        "'下一章'是真的下一章",
        "'下一页'是同一页",
        "看URL来定，最靠谱"
    ]
    for mnemonic in mnemonics:
        print(f"  {mnemonic}")
    print()


# ============================================
# 示例7: 常见HTML结构和解决方案
# ============================================

def example_html_structures():
    """
    常见HTML结构和解决方案示例

    展示常见的HTML结构及其对应的规则
    """

    structures = [
        {
            "类型": "标准列表（有封面）",
            "HTML": '<div class="book-list"><div class="item"><img src="cover.jpg" class="cover"/><a href="/book/1" class="title">书名</a></div></div>',
            "规则": {
                "bookList": ".book-list .item",
                "name": ".title@text",
                "coverUrl": "img@src",
                "bookUrl": "a@href"
            }
        },
        {
            "类型": "搜索页（无封面，信息合并）",
            "HTML": '<div class="hot_sale"><a href="/book/1"><p class="title">书名</p><p class="author">分类 | 作者：张三</p></a></div>',
            "规则": {
                "bookList": ".hot_sale",
                "name": ".title@text",
                "author": ".author.0@text##.*\\| |作者：##",
                "kind": ".author.0@text##\\|.*##",
                "coverUrl": "",
                "bookUrl": "a@href"
            }
        },
        {
            "类型": "懒加载图片",
            "HTML": '<img class="lazy" data-original="cover.jpg" src="placeholder.jpg"/>',
            "规则": {
                "coverUrl": "img.lazy@data-original||img@src"
            }
        },
    ]

    print("常见HTML结构和解决方案：")
    print()

    for structure in structures:
        print(f"{structure['类型']}:")
        print(f"  HTML: {structure['HTML'][:80]}...")
        print(f"  规则:")
        for key, value in structure['rules'].items():
            print(f"    {key}: {value}")
        print()


# ============================================
# 主函数
# ============================================

def main():
    """运行所有示例"""

    print("=" * 80)
    print("Legado Book Source Developer Skill - 工作流示例")
    print("=" * 80)
    print()

    # 运行示例
    example_create_book_source()
    example_css_selectors()
    example_regex_patterns()
    example_book_source_templates()
    example_encoding_detection()
    example_next_content_url()
    example_html_structures()

    print("=" * 80)
    print("示例演示完成")
    print("=" * 80)


if __name__ == "__main__":
    main()
