#!/usr/bin/env python3
"""一键部署打包 - 将蒸馏模型打包为可部署格式"""

import json
import shutil
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional
import zipfile
import tarfile


@dataclass
class DeploymentConfig:
    """部署配置"""
    model_name: str
    version: str
    format: str  # "hf", "gguf", "onnx", "tensorrt"
    quantization: Optional[str] = None  # "int8", "int4", None
    max_batch_size: int = 1
    max_seq_length: int = 8192
    device: str = "cuda"  # "cuda", "cpu", "auto"


class DeploymentPackager:
    """部署打包器"""

    def __init__(self, config: DeploymentConfig):
        self.config = config
        self.work_dir = Path(f"outputs/deploy_{config.model_name}")
        self.work_dir.mkdir(parents=True, exist_ok=True)

    def package(self, model_path: str, output_path: str) -> str:
        """主打包函数"""

        print(f"开始打包: {self.config.model_name} v{self.config.version}")
        print(f"格式: {self.config.format}")
        print(f"量化: {self.config.quantization or '无'}")

        # 根据格式选择打包方式
        if self.config.format == "hf":
            return self._package_huggingface(model_path, output_path)
        elif self.config.format == "gguf":
            return self._package_gguf(model_path, output_path)
        elif self.config.format == "onnx":
            return self._package_onnx(model_path, output_path)
        else:
            raise ValueError(f"不支持的格式: {self.config.format}")

    def _package_huggingface(self, model_path: str, output_path: str) -> str:
        """打包为HuggingFace格式"""

        model_dir = Path(model_path)
        output_dir = Path(output_path)

        # 复制模型文件
        if model_dir.exists():
            shutil.copytree(model_dir, output_dir, dirs_exist_ok=True)

        # 生成部署配置
        deploy_config = {
            "model_type": "distilled",
            "base_model": str(model_dir.name),
            "version": self.config.version,
            "max_batch_size": self.config.max_batch_size,
            "max_seq_length": self.config.max_seq_length,
            "honest_boundary": "HONEST_BOUNDARY.md",
            "inference": {
                "device": self.config.device,
                "dtype": "float16" if self.config.quantization is None else self.config.quantization
            }
        }

        with open(output_dir / "deployment_config.json", 'w') as f:
            json.dump(deploy_config, f, indent=2)

        # 生成推理示例代码
        self._generate_inference_example(output_dir)

        # 创建requirements.txt
        self._generate_requirements(output_dir)

        # 打包为zip
        zip_path = f"{output_path}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in output_dir.rglob("*"):
                zf.write(file, file.relative_to(output_dir.parent))

        print(f"HF格式打包完成: {zip_path}")
        return zip_path

    def _package_gguf(self, model_path: str, output_path: str) -> str:
        """打包为GGUF格式 (llama.cpp)"""

        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 生成转换脚本
        convert_script = f"""#!/bin/bash
# GGUF转换脚本 (需要llama.cpp)

LLAMA_CPP_PATH=${{LLAMA_CPP_PATH:-"./llama.cpp"}}

# 转换为GGUF
python $LLAMA_CPP_PATH/convert_hf_to_gguf.py \\
    {model_path} \\
    --outfile {output_dir}/{self.config.model_name}.gguf \\
    --outtype {self.config.quantization or "f16"}

echo "转换完成: {output_dir}/{self.config.model_name}.gguf"
"""
        with open(output_dir / "convert_to_gguf.sh", 'w') as f:
            f.write(convert_script)

        # 生成推理脚本
        inference_script = f"""#!/bin/bash
# GGUF推理脚本

./llama.cpp/llama-cli \\
    -m {self.config.model_name}.gguf \\
    -c {self.config.max_seq_length} \\
    -b {self.config.max_batch_size} \\
    --temp 0.7 \\
    -p "You are a helpful assistant."
"""
        with open(output_dir / "inference.sh", 'w') as f:
            f.write(inference_script)

        # 打包
        tar_path = f"{output_path}.tar.gz"
        with tarfile.open(tar_path, "w:gz") as tar:
            tar.add(output_dir, arcname=output_dir.name)

        print(f"GGUF格式打包完成: {tar_path}")
        print("注意: 需要手动运行convert_to_gguf.sh进行转换")
        return tar_path

    def _package_onnx(self, model_path: str, output_path: str) -> str:
        """打包为ONNX格式"""

        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 生成转换脚本
        convert_script = f"""#!/usr/bin/env python3
# ONNX转换脚本

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from pathlib import Path

model_path = "{model_path}"
output_path = "{output_dir}"

print("加载模型...")
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16,
    device_map="cpu"
)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# 准备示例输入
dummy_input = tokenizer("Hello, world!", return_tensors="pt")

print("导出ONNX...")
torch.onnx.export(
    model,
    (dummy_input["input_ids"],),
    f"{output_dir}/model.onnx",
    input_names=["input_ids"],
    output_names=["logits"],
    dynamic_axes={{
        "input_ids": {{0: "batch", 1: "sequence"}},
        "logits": {{0: "batch", 1: "sequence"}}
    }},
    opset_version=14
)

print(f"ONNX导出完成: {output_dir}/model.onnx")
"""
        with open(output_dir / "convert_to_onnx.py", 'w') as f:
            f.write(convert_script)

        # 打包
        tar_path = f"{output_path}.tar.gz"
        with tarfile.open(tar_path, "w:gz") as tar:
            tar.add(output_dir, arcname=output_dir.name)

        print(f"ONNX格式打包完成: {tar_path}")
        print("注意: 需要手动运行convert_to_onnx.py进行转换")
        return tar_path

    def _generate_inference_example(self, output_dir: Path):
        """生成推理示例代码"""

        example_code = '''#!/usr/bin/env python3
"""蒸馏模型推理示例"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def load_model(model_path: str):
    """加载蒸馏模型"""
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    return model, tokenizer

def generate(
    model,
    tokenizer,
    prompt: str,
    max_new_tokens: int = 512,
    temperature: float = 0.7,
    top_p: float = 0.9
) -> str:
    """生成回复"""

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=".", help="模型路径")
    parser.add_argument("--prompt", default="解释什么是知识蒸馏", help="输入提示")
    args = parser.parse_args()

    print("加载模型...")
    model, tokenizer = load_model(args.model)

    print(f"\\n提示: {args.prompt}\\n")
    print("生成中...")

    response = generate(model, tokenizer, args.prompt)
    print(f"\\n回复: {response}")
'''

        with open(output_dir / "inference_example.py", 'w') as f:
            f.write(example_code)

    def _generate_requirements(self, output_dir: Path):
        """生成依赖文件"""

        requirements = """torch>=2.0.0
transformers>=4.30.0
accelerate>=0.20.0
"""

        if self.config.format == "onnx":
            requirements += "onnx>=1.14.0\nonnxruntime>=1.15.0\n"

        with open(output_dir / "requirements.txt", 'w') as f:
            f.write(requirements)

        # 生成README
        readme = f"""# {self.config.model_name} - 蒸馏模型部署包

## 模型信息

- 名称: {self.config.model_name}
- 版本: {self.config.version}
- 格式: {self.config.format}
- 量化: {self.config.quantization or '无'}

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行推理

```bash
python inference_example.py --model . --prompt "你的问题"
```

### 使用 transformers

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(".")
tokenizer = AutoTokenizer.from_pretrained(".")
```

## 能力边界

请阅读 HONEST_BOUNDARY.md 了解本模型的适用场景和限制。

## 配置参数

- 最大序列长度: {self.config.max_seq_length}
- 最大批次大小: {self.config.max_batch_size}
- 推荐设备: {self.config.device}
"""

        with open(output_dir / "README.md", 'w') as f:
            f.write(readme)


def quick_deploy(model_path: str, output_dir: str = "outputs/deploy"):
    """快速部署入口"""

    config = DeploymentConfig(
        model_name="distilled_model",
        version="1.0.0",
        format="hf",
        quantization=None,
        max_batch_size=1,
        max_seq_length=8192,
        device="auto"
    )

    packager = DeploymentPackager(config)

    # 检查是否有评估结果
    eval_file = Path("outputs/evaluation/results.json")
    honest_boundary = Path("outputs/evaluation/HONEST_BOUNDARY.md")

    output_path = f"{output_dir}/{config.model_name}"
    package_path = packager.package(model_path, output_path)

    # 复制诚实边界文件
    if honest_boundary.exists():
        deploy_dir = Path(output_path)
        if deploy_dir.exists():
            shutil.copy(honest_boundary, deploy_dir / "HONEST_BOUNDARY.md")

    print(f"\\n✅ 部署包已生成: {package_path}")
    return package_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", required=True, help="模型路径")
    parser.add_argument("--output", default="outputs/deploy", help="输出目录")
    parser.add_argument("--format", default="hf", choices=["hf", "gguf", "onnx"])
    parser.add_argument("--quant", choices=["int8", "int4", "f16"], help="量化类型")
    parser.add_argument("--name", default="distilled_model", help="模型名称")
    parser.add_argument("--version", default="1.0.0", help="版本号")
    args = parser.parse_args()

    config = DeploymentConfig(
        model_name=args.name,
        version=args.version,
        format=args.format,
        quantization=args.quant,
        max_batch_size=1,
        max_seq_length=8192
    )

    packager = DeploymentPackager(config)
    output_path = f"{args.output}/{args.name}"

    packager.package(args.model_path, output_path)
