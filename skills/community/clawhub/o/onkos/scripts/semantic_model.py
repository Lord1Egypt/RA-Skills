#!/usr/bin/env python3
"""
语义模型管理器 - 下载、加载和推理 ONNX 语义向量模型
基于 text2vec-base-chinese (chinese-macbert-base + CoSENT)
支持首次自动下载，本地缓存，ONNX Runtime 推理
"""

import os
import json
import argparse
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

# 检测 ONNX Runtime
try:
    import onnxruntime as ort
    import numpy as np
    ONNX_AVAILABLE = True
except ImportError:
    ONNX_AVAILABLE = False


# ==================== 轻量级 BERT 分词器 ====================

class BasicTokenizer:
    """基础分词器 - 处理空白符、CJK 字符拆分、标点符号"""

    def __init__(self, do_lower_case: bool = True):
        self.do_lower_case = do_lower_case

    def tokenize(self, text: str) -> List[str]:
        text = self._clean_text(text)
        text = self._tokenize_chinese_chars(text)
        orig_tokens = text.strip().split()
        if self.do_lower_case:
            orig_tokens = [t.lower() for t in orig_tokens]
        tokens = []
        for token in orig_tokens:
            token = self._run_strip_accents(token)
            tokens.extend(self._run_split_on_punctuation(token))
        return " ".join(tokens).strip().split()

    def _clean_text(self, text: str) -> str:
        output = []
        for ch in text:
            cp = ord(ch)
            if cp == 0 or cp == 0xFFFD or self._is_control(ch):
                continue
            if self._is_whitespace(ch):
                output.append(" ")
            else:
                output.append(ch)
        return "".join(output)

    def _tokenize_chinese_chars(self, text: str) -> str:
        output = []
        for ch in text:
            cp = ord(ch)
            if self._is_chinese_char(cp):
                output.append(" ")
                output.append(ch)
                output.append(" ")
            else:
                output.append(ch)
        return "".join(output)

    @staticmethod
    def _is_chinese_char(cp: int) -> bool:
        return ((0x4E00 <= cp <= 0x9FFF) or
                (0x3400 <= cp <= 0x4DBF) or
                (0x20000 <= cp <= 0x2A6DF) or
                (0x2A700 <= cp <= 0x2B73F) or
                (0x2B740 <= cp <= 0x2B81F) or
                (0x2B820 <= cp <= 0x2CEAF) or
                (0xF900 <= cp <= 0xFAFF) or
                (0x2F800 <= cp <= 0x2FA1F))

    def _run_strip_accents(self, text: str) -> str:
        text = unicodedata.normalize("NFD", text)
        output = []
        for ch in text:
            cat = unicodedata.category(ch)
            if cat == "Mn":
                continue
            output.append(ch)
        return "".join(output)

    def _run_split_on_punctuation(self, text: str) -> List[str]:
        tokens = []
        start_new = True
        for ch in text:
            if self._is_punctuation(ch):
                tokens.append([ch])
                start_new = True
            else:
                if start_new:
                    tokens.append([])
                    start_new = False
                tokens[-1].append(ch)
        return ["".join(t) for t in tokens]

    @staticmethod
    def _is_punctuation(ch: str) -> bool:
        cp = ord(ch)
        if (33 <= cp <= 47) or (58 <= cp <= 64) or (91 <= cp <= 96) or (123 <= cp <= 126):
            return True
        cat = unicodedata.category(ch)
        return cat.startswith("P")

    @staticmethod
    def _is_whitespace(ch: str) -> bool:
        if ch in (" ", "\t", "\n", "\r"):
            return True
        cat = unicodedata.category(ch)
        return cat == "Zs"

    @staticmethod
    def _is_control(ch: str) -> bool:
        if ch in ("\t", "\n", "\r"):
            return False
        cat = unicodedata.category(ch)
        return cat.startswith("C")


class WordPieceTokenizer:
    """WordPiece 子词分词器"""

    def __init__(self, vocab: Dict[str, int], unk_token: str = "[UNK]",
                 max_input_chars_per_word: int = 200):
        self.vocab = vocab
        self.unk_token = unk_token
        self.max_input_chars_per_word = max_input_chars_per_word

    def tokenize(self, text: str) -> List[str]:
        output_tokens = []
        for token in text.strip().split():
            chars = list(token)
            if len(chars) > self.max_input_chars_per_word:
                output_tokens.append(self.unk_token)
                continue
            is_bad = False
            start = 0
            sub_tokens = []
            while start < len(chars):
                end = len(chars)
                cur_substr = None
                while start < end:
                    substr = "".join(chars[start:end])
                    if start > 0:
                        substr = "##" + substr
                    if substr in self.vocab:
                        cur_substr = substr
                        break
                    end -= 1
                if cur_substr is None:
                    is_bad = True
                    break
                sub_tokens.append(cur_substr)
                start = end
            if is_bad:
                output_tokens.append(self.unk_token)
            else:
                output_tokens.extend(sub_tokens)
        return output_tokens


class BertTokenizerLite:
    """轻量级 BERT 分词器 - 仅需 vocab.txt，无需 transformers 依赖"""

    CLS_TOKEN = "[CLS]"
    SEP_TOKEN = "[SEP]"
    PAD_TOKEN = "[PAD]"
    UNK_TOKEN = "[UNK]"

    def __init__(self, vocab_path: str, do_lower_case: bool = True,
                 max_seq_length: int = 128):
        self.vocab = self._load_vocab(vocab_path)
        self.ids_to_tokens = {v: k for k, v in self.vocab.items()}
        self.basic_tokenizer = BasicTokenizer(do_lower_case=do_lower_case)
        self.wordpiece_tokenizer = WordPieceTokenizer(self.vocab, self.UNK_TOKEN)
        self.max_seq_length = max_seq_length

        self.cls_id = self.vocab.get(self.CLS_TOKEN, 101)
        self.sep_id = self.vocab.get(self.SEP_TOKEN, 102)
        self.pad_id = self.vocab.get(self.PAD_TOKEN, 0)

    @staticmethod
    def _load_vocab(vocab_path: str) -> Dict[str, int]:
        vocab = {}
        with open(vocab_path, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f):
                token = line.strip()
                if token:
                    vocab[token] = idx
        return vocab

    def encode(self, text: str, max_length: int = None) -> Dict[str, Any]:
        """
        编码文本为 BERT 输入格式

        Args:
            text: 输入文本
            max_length: 最大序列长度

        Returns:
            dict: input_ids, attention_mask, token_type_ids
        """
        max_length = max_length or self.max_seq_length

        basic_tokens = self.basic_tokenizer.tokenize(text)
        wp_tokens = self.wordpiece_tokenizer.tokenize(" ".join(basic_tokens))

        # 截断（保留 [CLS] + [SEP] 的空间）
        if len(wp_tokens) > max_length - 2:
            wp_tokens = wp_tokens[:max_length - 2]

        # 添加特殊标记
        tokens = [self.CLS_TOKEN] + wp_tokens + [self.SEP_TOKEN]
        input_ids = [self.vocab.get(t, self.vocab.get(self.UNK_TOKEN, 100)) for t in tokens]
        token_type_ids = [0] * len(input_ids)
        attention_mask = [1] * len(input_ids)

        # 填充到 max_length
        pad_len = max_length - len(input_ids)
        if pad_len > 0:
            input_ids += [self.pad_id] * pad_len
            token_type_ids += [0] * pad_len
            attention_mask += [0] * pad_len

        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "token_type_ids": token_type_ids
        }

    def encode_batch(self, texts: List[str], max_length: int = None) -> Dict[str, Any]:
        """批量编码文本"""
        encoded = [self.encode(t, max_length) for t in texts]
        return {
            "input_ids": [e["input_ids"] for e in encoded],
            "attention_mask": [e["attention_mask"] for e in encoded],
            "token_type_ids": [e["token_type_ids"] for e in encoded]
        }


# ==================== 语义模型管理 ====================

_SETTINGS_JSON_EXAMPLE = """\
{
  "model_repo": "shibing624/text2vec-base-chinese",
  "files": {
    "int8": {"candidate": "onnx/model_qint8_avx512_vnni.onnx", "local_name": "model_qint8_avx512_vnni.onnx"}
  },
  "embedding_dim": 768,
  "max_seq_length": 128,
  "sha256": {
    "model_qint8_avx512_vnni.onnx": "<填入SHA256>"
  },
  "download_sources": [
    {"name": "HF-Mirror",   "base_url": "https://hf-mirror.com/shibing624/text2vec-base-chinese/resolve/main",  "path_type": "repo"},
    {"name": "HuggingFace", "base_url": "https://huggingface.co/shibing624/text2vec-base-chinese/resolve/main",  "path_type": "repo"}
  ]
}"""


def _load_model_config() -> dict:
    """从 assets/model/settings.json 加载模型下载配置"""
    config_path = Path(__file__).parent.parent / "assets" / "model" / "settings.json"
    if not config_path.exists():
        print(f"[ERROR] 模型配置文件缺失: {config_path}")
        print("[解决] 请尝试以下方案:")
        print("  1. 更新 onkos 技能至最新版，恢复内置配置文件")
        print(f"  2. 手动创建配置文件，路径: {config_path}")
        print(f"  配置文件格式示例:\n{_SETTINGS_JSON_EXAMPLE}")
        return {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"[ERROR] 模型配置文件损坏: {config_path}")
        print(f"  解析失败: {e}")
        print("[解决] 请尝试以下方案:")
        print("  1. 更新 onkos 技能至最新版，恢复内置配置文件")
        print(f"  2. 删除损坏文件后手动创建，路径: {config_path}")
        print(f"  配置文件格式示例:\n{_SETTINGS_JSON_EXAMPLE}")
        return {}


_MODEL_CONFIG = _load_model_config()


class SemanticModel:
    """语义向量模型管理器 - 下载、加载、推理"""

    # 从 assets/model/settings.json 加载
    MODEL_CONFIG = _MODEL_CONFIG
    DOWNLOAD_SOURCES = _MODEL_CONFIG.get("download_sources", [])
    SHA256 = _MODEL_CONFIG.get("sha256", {})
    EMBEDDING_DIM = _MODEL_CONFIG.get("embedding_dim", 768)
    MAX_SEQ_LENGTH = _MODEL_CONFIG.get("max_seq_length", 128)
    # ONNX 候选文件键（按优先级），int8 优先，fp32 备用
    ONNX_CANDIDATE_KEYS = [k for k in ["int8", "fp32"] if k in _MODEL_CONFIG.get("files", {})]

    def __init__(self, model_dir: str = None):
        """
        初始化语义模型管理器

        Args:
            model_dir: 模型文件存储目录。默认为 assets/model
        """
        if model_dir:
            self.model_dir = Path(model_dir)
        else:
            self.model_dir = Path(__file__).parent.parent / "assets" / "model"

        self._session = None
        self._tokenizer = None
        self._model_file = None

    @property
    def is_ready(self) -> bool:
        """模型是否可用"""
        return ONNX_AVAILABLE and self._find_onnx_file() is not None and self._vocab_exists()

    def _vocab_exists(self) -> bool:
        return (self.model_dir / "vocab.txt").exists()

    def _find_onnx_file(self) -> Optional[Path]:
        """查找已下载的 ONNX 模型文件"""
        files_cfg = self.MODEL_CONFIG.get("files", {})
        # 按 ONNX 候选优先级查找本地文件
        for key in self.ONNX_CANDIDATE_KEYS:
            local_name = files_cfg[key]["local_name"]
            p = self.model_dir / local_name
            if p.exists() and p.stat().st_size > 1000:
                return p
        # 也搜索任意 .onnx 文件
        if self.model_dir.exists():
            for f in self.model_dir.glob("*.onnx"):
                if f.stat().st_size > 1000:
                    return f
        # 检查外部数据模式（model.onnx + model.onnx.data）
        data_file = self.model_dir / "model.onnx.data"
        onnx_file = self.model_dir / "model.onnx"
        if data_file.exists() and onnx_file.exists():
            return onnx_file
        return None

    def _build_url(self, source: dict, file_cfg: dict) -> str:
        """根据源的 path_type 构建下载 URL
        repo: 用 candidate（含 onnx/ 子目录路径）
        flat: 用 local_name（平铺路径）
        """
        path_type = source.get("path_type", "repo")
        remote_path = file_cfg["candidate"] if path_type == "repo" else file_cfg["local_name"]
        return f"{source['base_url']}/{remote_path}"

    def download(self, verbose: bool = True) -> bool:
        """
        下载 ONNX 模型文件到本地（自动尝试多个镜像源）
        vocab.txt 和 config.json 已内置在 assets/model/ 中，无需下载

        Args:
            verbose: 是否打印下载进度

        Returns:
            是否下载成功
        """
        if not ONNX_AVAILABLE:
            if verbose:
                print("错误: onnxruntime 未安装，无法使用语义模型")
            return False

        self.model_dir.mkdir(parents=True, exist_ok=True)
        files_cfg = self.MODEL_CONFIG.get("files", {})

        # 下载 ONNX 模型（按候选优先级尝试，任一成功即可）
        onnx_downloaded = self._find_onnx_file()
        onnx_corrupted = False
        if onnx_downloaded is not None:
            local_name = onnx_downloaded.name
            expected_hash = self.SHA256.get(local_name)
            if expected_hash and not self._sha256_verify(onnx_downloaded, expected_hash, verbose=False):
                if verbose:
                    print(f"已存在模型校验失败，将重新下载: {local_name}")
                onnx_corrupted = True
                onnx_downloaded = None
        if onnx_downloaded is None:
            for key in self.ONNX_CANDIDATE_KEYS:
                file_cfg = files_cfg[key]
                local_name = file_cfg["local_name"]
                target = self.model_dir / local_name
                tmp_target = self.model_dir / f"{local_name}.downloading"
                for source in self.DOWNLOAD_SOURCES:
                    url = self._build_url(source, file_cfg)
                    if verbose:
                        print(f"下载 {file_cfg['candidate']} ...（{source['name']}，文件较大，可能需要几分钟）")
                    if self._download_file(url, tmp_target, verbose):
                        expected_hash = self.SHA256.get(local_name)
                        if expected_hash and not self._sha256_verify(tmp_target, expected_hash, verbose):
                            tmp_target.unlink(missing_ok=True)
                            if verbose:
                                print(f"  下载模型校验失败，尝试下一个源")
                            continue
                        if target.exists():
                            target.unlink()
                        tmp_target.rename(target)
                        onnx_downloaded = target
                        onnx_corrupted = False
                        break
                    else:
                        if tmp_target.exists():
                            tmp_target.unlink()
                        if verbose:
                            print(f"  {source['name']}下载 {file_cfg['candidate']} 失败")

                if onnx_downloaded:
                    break

        if onnx_downloaded is None:
            # 如果原有文件被标记为校验失败但重新下载也失败，保留原文件（降级使用）
            if onnx_corrupted and self._find_onnx_file() is not None:
                if verbose:
                    print("警告: 模型文件校验失败且重新下载失败，保留原文件（存在安全风险）")
                onnx_downloaded = self._find_onnx_file()
            else:
                print("所有 ONNX 模型下载均失败（所有镜像源均不可用或校验未通过）")
                return False

        if verbose:
            size_mb = onnx_downloaded.stat().st_size / (1024 * 1024)
            print(f"模型下载完成: {onnx_downloaded.name} ({size_mb:.1f}MB)")

        return True

    @staticmethod
    def _sha256_verify(filepath, expected_hash: str, verbose: bool = True) -> bool:
        """校验文件 SHA256 哈希值，防止供应链攻击"""
        import hashlib
        sha256 = hashlib.sha256()
        filepath = Path(filepath) if not isinstance(filepath, Path) else filepath
        try:
            with open(filepath, "rb") as f:
                while True:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    sha256.update(chunk)
            actual = sha256.hexdigest()
            if actual == expected_hash:
                if verbose:
                    print(f"  完整性校验通过: {filepath.name}")
                return True
            else:
                if verbose:
                    print(f"  完整性校验失败: {filepath.name}")
                    print(f"    预期: {expected_hash}")
                    print(f"    实际: {actual}")
                return False
        except Exception as e:
            if verbose:
                print(f"  校验出错: {e}")
            return False

    @staticmethod
    def _download_file(url: str, target: Path, verbose: bool = True) -> bool:
        """下载单个文件，优先用 curl（处理重定向更可靠），降级到 urllib"""
        import subprocess

        # 优先使用 curl（更可靠地处理 HuggingFace 的 307 重定向）
        try:
            result = subprocess.run(
                ["curl", "-sL", "--connect-timeout", "30", "--max-time", "600",
                 "-o", str(target), url],
                capture_output=True, timeout=620
            )
            if result.returncode == 0 and target.exists() and target.stat().st_size > 100:
                if verbose:
                    size_kb = target.stat().st_size / 1024
                    print(f"  完成 ({size_kb:.1f}KB)")
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass  # curl 不可用，降级

        # 降级到 urllib
        import urllib.request
        import socket

        try:
            tmp_path = target.with_suffix(target.suffix + ".tmp")

            def _reporthook(count, block_size, total_size):
                if verbose and total_size > 0:
                    downloaded = count * block_size
                    percent = min(downloaded / total_size * 100, 100)
                    mb = downloaded / (1024 * 1024)
                    total_mb = total_size / (1024 * 1024)
                    print(f"\r  进度: {percent:.1f}% ({mb:.1f}/{total_mb:.1f}MB)", end="", flush=True)

            old_timeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(60)
            try:
                urllib.request.urlretrieve(url, str(tmp_path), _reporthook)
            finally:
                socket.setdefaulttimeout(old_timeout)

            if verbose:
                print()

            if not tmp_path.exists() or tmp_path.stat().st_size < 100:
                if tmp_path.exists():
                    tmp_path.unlink()
                return False

            tmp_path.rename(target)
            return True

        except Exception as e:
            if verbose:
                print(f"\n下载错误: {e}")
            for tmp in target.parent.glob(target.name + "*.tmp"):
                tmp.unlink(missing_ok=True)
            return False

    def _load_model(self):
        """延迟加载模型和分词器"""
        if self._session is not None:
            return True

        onnx_file = self._find_onnx_file()
        if onnx_file is None or not self._vocab_exists():
            return False

        try:
            # 加载分词器
            self._tokenizer = BertTokenizerLite(str(self.model_dir / "vocab.txt"))
            self._model_file = onnx_file

            # 加载 ONNX 模型
            sess_options = ort.SessionOptions()
            sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
            self._session = ort.InferenceSession(
                str(onnx_file), sess_options,
                providers=["CPUExecutionProvider"]
            )
            return True
        except Exception as e:
            self._session = None
            self._tokenizer = None
            return False

    def encode(self, text: str) -> Optional[Any]:
        """
        编码文本为语义向量

        Args:
            text: 输入文本

        Returns:
            numpy 数组 (768,) 或 None
        """
        if not ONNX_AVAILABLE:
            return None

        if not self._load_model():
            return None

        try:
            encoded = self._tokenizer.encode(text)
            input_ids = np.array([encoded["input_ids"]], dtype=np.int64)
            attention_mask = np.array([encoded["attention_mask"]], dtype=np.int64)
            token_type_ids = np.array([encoded["token_type_ids"]], dtype=np.int64)

            outputs = self._session.run(
                None,
                {
                    "input_ids": input_ids,
                    "attention_mask": attention_mask,
                    "token_type_ids": token_type_ids
                }
            )

            # Mean Pooling
            token_embeddings = outputs[0]  # (1, seq_len, hidden_size)
            mask = attention_mask[:, :, np.newaxis].astype(np.float32)
            embedding = np.sum(token_embeddings * mask, axis=1) / np.clip(mask.sum(axis=1), 1e-9, None)

            # L2 归一化
            norm = np.linalg.norm(embedding, axis=1, keepdims=True)
            embedding = embedding / np.clip(norm, 1e-9, None)

            return embedding[0]  # (768,)

        except Exception:
            return None

    def encode_batch(self, texts: List[str], batch_size: int = 8) -> List[Optional[Any]]:
        """
        批量编码文本为语义向量

        Args:
            texts: 输入文本列表
            batch_size: 批处理大小

        Returns:
            向量列表
        """
        if not ONNX_AVAILABLE or not self._load_model():
            return [None] * len(texts)

        results = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            try:
                encoded = self._tokenizer.encode_batch(batch)
                input_ids = np.array(encoded["input_ids"], dtype=np.int64)
                attention_mask = np.array(encoded["attention_mask"], dtype=np.int64)
                token_type_ids = np.array(encoded["token_type_ids"], dtype=np.int64)

                outputs = self._session.run(
                    None,
                    {
                        "input_ids": input_ids,
                        "attention_mask": attention_mask,
                        "token_type_ids": token_type_ids
                    }
                )

                token_embeddings = outputs[0]
                mask = attention_mask[:, :, np.newaxis].astype(np.float32)
                embeddings = np.sum(token_embeddings * mask, axis=1) / np.clip(mask.sum(axis=1), 1e-9, None)
                norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
                embeddings = embeddings / np.clip(norms, 1e-9, None)

                for j in range(len(batch)):
                    results.append(embeddings[j])

            except Exception:
                results.extend([None] * len(batch))

        return results

    def get_status(self) -> Dict[str, Any]:
        """获取模型状态信息"""
        onnx_file = self._find_onnx_file()
        return {
            "onnx_available": ONNX_AVAILABLE,
            "model_dir": str(self.model_dir),
            "model_file": onnx_file.name if onnx_file else None,
            "model_size_mb": round(onnx_file.stat().st_size / (1024 * 1024), 1) if onnx_file else None,
            "vocab_exists": self._vocab_exists(),
            "is_ready": self.is_ready,
            "loaded": self._session is not None
        }


def main():
    parser = argparse.ArgumentParser(description='语义模型管理器')
    parser.add_argument('--model-dir', help='模型文件存储目录')
    parser.add_argument('--action', required=True,
                       choices=['download', 'status', 'test', 'encode'],
                       help='操作类型')
    parser.add_argument('--text', help='待编码文本')
    parser.add_argument('--output', choices=['text', 'json'], default='json')

    args = parser.parse_args()
    model = SemanticModel(args.model_dir)

    result = None

    if args.action == 'download':
        success = model.download(verbose=True)
        result = {"downloaded": success, "is_ready": model.is_ready}

    elif args.action == 'status':
        result = model.get_status()

    elif args.action == 'test':
        if not model.is_ready:
            result = {"error": "模型未就绪，请先执行 download 操作"}
        else:
            test_text = "这是一个测试句子"
            vec = model.encode(test_text)
            if vec is not None:
                result = {
                    "test_text": test_text,
                    "vector_dim": len(vec),
                    "vector_norm": float(np.linalg.norm(vec)),
                    "first_5": [round(float(v), 4) for v in vec[:5]]
                }
            else:
                result = {"error": "编码失败"}

    elif args.action == 'encode':
        if not args.text:
            result = {"error": "需要提供 --text 参数"}
        else:
            vec = model.encode(args.text)
            if vec is not None:
                result = {
                    "text": args.text,
                    "vector_dim": len(vec),
                    "vector": [round(float(v), 6) for v in vec]
                }
            else:
                result = {"error": "编码失败，模型可能未就绪"}

    if args.output == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == '__main__':
    main()
