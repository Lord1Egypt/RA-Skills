def summarize_key_points(text: str, length: str = "normal"):
    # 1. 输入校验
    if not text or len(text.strip()) == 0:
        return {"error": "文本不能为空"}

    # 2. 这里替换成你实际调用的模型/API
    summary = f"这是{length}模式总结：\n{text[:100]}..."
    key_points = [
        "要点1：xxx",
        "要点2：yyy",
        "要点3：zzz"
    ]

    # 3. 结构化输出（Agent 最爱这种格式）
    return {
        "summary": summary,
        "key_points": key_points,
        "original_length": len(text),
        "output_length": len(summary)
    }


if __name__ == "__main__":
    test_text = "这是一段很长很长的文本..."
    result = summarize_key_points(test_text, "normal")
    print(result)