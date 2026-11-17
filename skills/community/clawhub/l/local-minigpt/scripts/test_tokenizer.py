# -*- coding: utf-8 -*-
"""分词器单元测试:python minigpt/test_tokenizer.py"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tokenizer import CharTokenizer


def main() -> None:
    sample = "你好,世界!Hello, GPT。\n第二行"
    tok = CharTokenizer.from_text(sample)
    assert tok.vocab_size == len(set(sample)), "词表大小错误"

    ids = tok.encode("世界Hello")
    assert tok.decode(ids) == "世界Hello", "往返编码失败"

    # 词表外字符应被跳过(x/y/z 不在样本文本中)
    assert tok.decode(tok.encode("世界xyz Hello")) == "世界 Hello", "未知字符处理错误"

    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "tok.json"
        tok.save(str(p))
        tok2 = CharTokenizer.load(str(p))
        assert tok2.chars == tok.chars, "保存/加载后词表不一致"
        assert tok2.decode(tok2.encode(sample)) == sample, "加载后往返编码失败"

    print(f"test_tokenizer: 全部通过(vocab={tok.vocab_size})")


if __name__ == "__main__":
    main()
