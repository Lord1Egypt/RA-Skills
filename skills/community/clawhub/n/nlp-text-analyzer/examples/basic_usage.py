"""
NLP Text Analyzer - 使用示例
演示文本分析器的各种功能
"""

from scripts.text_analyzer import TextAnalyzer, TextClassifier, AnalysisResult


def example_language_detection():
    """
    语言检测示例
    """
    print("=" * 60)
    print("示例1: 语言检测")
    print("=" * 60)
    
    analyzer = TextAnalyzer()
    
    texts = [
        "这是一个中文文本示例",
        "This is an English text example",
        "This is mixed 中文和English文本",
        "123 456 !@#$"  # 无法检测
    ]
    
    for text in texts:
        lang = analyzer.detect_language(text)
        print(f"文本: {text[:30]}... -> 语言: {lang}")


def example_segmentation():
    """
    分词示例
    """
    print("\n" + "=" * 60)
    print("示例2: 文本分词")
    print("=" * 60)
    
    analyzer = TextAnalyzer()
    
    # 中文分词
    chinese_text = "自然语言处理是人工智能的一个重要分支，它研究如何实现人与计算机之间用自然语言进行有效通信。"
    tokens = analyzer.segment(chinese_text)
    print(f"中文分词结果:\n{tokens[:15]}...")
    print(f"总词数: {len(tokens)}")
    
    # 英文分词
    english_text = "Natural language processing (NLP) is a branch of artificial intelligence."
    tokens_en = analyzer.segment(english_text)
    print(f"\n英文分词结果:\n{tokens_en}")


def example_sentiment_analysis():
    """
    情感分析示例
    """
    print("\n" + "=" * 60)
    print("示例3: 情感分析")
    print("=" * 60)
    
    analyzer = TextAnalyzer()
    
    texts = [
        "这个产品真的很棒！我非常喜欢。",
        "这个服务太糟糕了，完全不满意。",
        "今天的天气还不错。",
        "This product is amazing! I love it.",
        "The service was terrible and disappointing.",
        "The weather today is quite pleasant."
    ]
    
    for text in texts:
        result = analyzer.analyze_sentiment(text)
        sentiment = "正面" if result.polarity > 0 else "负面" if result.polarity < 0 else "中性"
        print(f"\n文本: {text[:30]}...")
        print(f"  语言: {result.language}, 极性: {result.polarity}, 主观性: {result.subjectivity}")
        print(f"  情感倾向: {sentiment} (置信度: {result.confidence})")


def example_keyword_extraction():
    """
    关键词提取示例
    """
    print("\n" + "=" * 60)
    print("示例4: 关键词提取")
    print("=" * 60)
    
    analyzer = TextAnalyzer()
    
    text = """
    人工智能（AI）是计算机科学的一个分支，它企图了解智能的实质，
    并生产出一种新的能以人类智能相似的方式做出反应的智能机器。
    该领域的研究包括机器人、语音识别、图像识别、自然语言处理和专家系统等。
    """
    
    keywords = analyzer.extract_keywords(text, top_k=10)
    print("中文关键词提取:")
    for word, weight in keywords:
        print(f"  - {word}: {weight}")
    
    # 英文关键词提取
    en_text = """
    Artificial Intelligence (AI) is a branch of computer science that aims to create 
    intelligent machines capable of performing tasks that typically require human intelligence. 
    These tasks include visual perception, speech recognition, decision-making, 
    and translation between languages.
    """
    
    keywords_en = analyzer.extract_keywords(en_text, top_k=8)
    print("\n英文关键词提取:")
    for word, weight in keywords_en:
        print(f"  - {word}: {weight}")


def example_text_summarization():
    """
    文本摘要示例
    """
    print("\n" + "=" * 60)
    print("示例5: 文本摘要")
    print("=" * 60)
    
    analyzer = TextAnalyzer()
    
    long_text = """
    深度学习是机器学习的一种，而机器学习是实现人工智能的必经路径。
    深度学习的概念源于人工神经网络的研究。含多隐层的多层感知器就是一种深度学习结构。
    深度学习通过组合低层特征形成更加抽象的高层表示属性类别或特征，以发现数据的分布式特征表示。
    研究深度学习的动机在于建立模拟人脑进行分析学习的神经网络，它模仿人脑的机制来解释数据，
    例如图像，声音和文本。深度学习的概念由Hinton等人于2006年提出。
    基于深信度网（DBN）提出非监督贪心逐层训练算法，为解决深层结构相关的优化难题带来希望。
    随后提出多层自动编码器深层结构。此外Lecun等人提出的卷积神经网络是第一个真正多层结构学习算法，
    它利用空间相对关系减少参数数目以提高训练性能。
    """
    
    summary = analyzer.generate_summary(long_text, num_sentences=2)
    print("原文长度:", len(long_text))
    print("摘要长度:", len(summary))
    print("\n生成的摘要:")
    print(summary)


def example_word_frequency():
    """
    词频统计示例
    """
    print("\n" + "=" * 60)
    print("示例6: 词频统计")
    print("=" * 60)
    
    analyzer = TextAnalyzer()
    
    text = """
    数据科学是一门利用数据学习知识的学科，其目标是通过从数据中提取有价值的部分来生产数据产品。
    它结合了诸多领域中的理论和技术，包括应用数学、统计、模式识别、机器学习、数据可视化、
    数据仓库以及高性能计算。数据科学通过运用各种相关的数据来帮助非专业人士理解问题。
    """
    
    freq = analyzer.word_frequency(text, top_k=15)
    print("词频统计 (Top 15):")
    for word, count in freq.items():
        print(f"  {word}: {count}")


def example_similarity():
    """
    相似度计算示例
    """
    print("\n" + "=" * 60)
    print("示例7: 文本相似度计算")
    print("=" * 60)
    
    analyzer = TextAnalyzer()
    
    texts = [
        ("自然语言处理是人工智能的重要分支", 
         "NLP是AI领域的重要研究方向"),
        ("今天天气很好", 
         "今天天气不错"),
        ("苹果是一种水果", 
         "苹果公司发布了新产品")
    ]
    
    for text1, text2 in texts:
        cosine_sim = analyzer.calculate_similarity(text1, text2, method='cosine')
        jaccard_sim = analyzer.calculate_similarity(text1, text2, method='jaccard')
        print(f"\n文本1: {text1}")
        print(f"文本2: {text2}")
        print(f"  余弦相似度: {cosine_sim}")
        print(f"  Jaccard相似度: {jaccard_sim}")


def example_comprehensive_analysis():
    """
    综合分析示例
    """
    print("\n" + "=" * 60)
    print("示例8: 综合文本分析")
    print("=" * 60)
    
    analyzer = TextAnalyzer()
    
    text = """
    机器学习是人工智能的一个分支，它使计算机能够在没有明确编程的情况下学习。
    机器学习算法通过从数据中发现模式来做出预测和决策。
    深度学习是机器学习的一个子集，使用神经网络模拟人脑的工作方式。
    这些技术在图像识别、语音识别、自然语言处理等领域取得了巨大成功。
    ""
    
    result = analyzer.analyze(text)
    
    print(f"检测语言: {result.language}")
    print(f"文本长度: {result.text_length} 字符")
    print(f"句子数量: {result.sentence_count}")
    print(f"分词数量: {len(result.tokens)}")
    print(f"\n情感分析:")
    print(f"  极性: {result.sentiment.polarity}")
    print(f"  主观性: {result.sentiment.subjectivity}")
    print(f"\n关键词 (Top 5):")
    for word, weight in result.keywords[:5]:
        print(f"  - {word}: {weight}")
    print(f"\n高频词:")
    for word, count in list(result.word_freq.items())[:5]:
        print(f"  - {word}: {count}")
    print(f"\n摘要:\n{result.summary}")


def example_text_classification():
    """
    文本分类示例
    """
    print("\n" + "=" * 60)
    print("示例9: 文本分类")
    print("=" * 60)
    
    analyzer = TextAnalyzer()
    classifier = TextClassifier()
    
    # 定义分类和关键词
    classifier.add_category("科技", ["人工智能", "机器学习", "深度学习", "算法", "神经网络", "AI", "机器学习", "技术"])
    classifier.add_category("体育", ["比赛", "运动员", "冠军", "球队", "体育", "联赛", "世界杯"])
    classifier.add_category("财经", ["股票", "投资", "市场", "经济", "金融", "公司", "利润"])
    
    texts = [
        "深度学习算法在图像识别领域取得了突破性进展",
        "股市今日大涨，科技股表现强劲",
        "国家队在世界杯预选赛中取得胜利"
    ]
    
    for text in texts:
        results = classifier.classify(text, analyzer)
        print(f"\n文本: {text}")
        print("分类结果:")
        for cat, score in results:
            print(f"  - {cat}: {score * 100:.1f}%")


if __name__ == "__main__":
    print("NLP文本分析器 - 使用示例\n")
    
    example_language_detection()
    example_segmentation()
    example_sentiment_analysis()
    example_keyword_extraction()
    example_text_summarization()
    example_word_frequency()
    example_similarity()
    example_comprehensive_analysis()
    example_text_classification()
    
    print("\n" + "=" * 60)
    print("所有示例执行完成")
    print("=" * 60)
