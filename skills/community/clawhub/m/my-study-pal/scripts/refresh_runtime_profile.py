# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import re


def section(text: str, heading: str) -> str:
    pattern = rf"(?ms)^## {re.escape(heading)}\s*(.*?)(?=^## |\Z)"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else "- 暂无记录"


def subsection(text: str, heading: str) -> str:
    pattern = rf"(?ms)^### {re.escape(heading)}\s*(.*?)(?=^### |^## |\Z)"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else "- 暂无记录"


def main() -> None:
    parser = argparse.ArgumentParser(description="Refresh mystudy/runtime-profile.md")
    parser.add_argument("--root", default=".", help="Workspace root containing mystudy/")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    study_root = root / "mystudy"
    user_profile_path = study_root / "user-profile.md"
    runtime_path = study_root / "runtime-profile.md"

    if not user_profile_path.exists():
        raise SystemExit(
            f"Missing user profile: {user_profile_path}. Run scripts/init_mystudy.ps1 first."
        )

    profile = user_profile_path.read_text(encoding="utf-8")

    work = section(profile, "用户工作 / 专业 / 业务领域")
    hobbies = section(profile, "用户爱好领域")
    recent = section(profile, "用户最近的 5 个学习知识点")
    direct = subsection(profile, "直答模式")
    expository = subsection(profile, "讲解式")
    guided = subsection(profile, "引导式")
    contrastive = subsection(profile, "辨析式")
    applied = subsection(profile, "场景应用式")
    retention = subsection(profile, "记忆巩固式")
    style = section(profile, "语言风格偏好")
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    runtime = f"""# 当前生效学习配置

> 本文件由 `mystudy/user-profile.md` 派生，刷新时间：{generated_at}。
> `user-profile.md` 是源头；用户长期偏好变化时，先更新 `user-profile.md`，再刷新本文件。

## 回答方式默认策略

- 简单、直接、单点事实型问题：直答模式
- 名词概念解释、缩写还原、快速听懂类问题：讲解式
- 原理机制、过程推演、因果链分析、深入拆解类问题：引导式
- 概念区别、边界判断、相近词辨析类问题：辨析式
- 概念落地、工作应用、行动建议类问题：场景应用式
- 记忆、复习、巩固、避免遗忘类问题：记忆巩固式

## 用户语境摘要

### 用户工作 / 专业 / 业务领域
{work}

### 用户爱好领域
{hobbies}

### 用户最近的 5 个学习知识点
{recent}

## 直答模式生效配置
{direct}

## 讲解式生效配置
{expository}

## 引导式生效配置
{guided}

## 辨析式生效配置
{contrastive}

## 场景应用式生效配置
{applied}

## 记忆巩固式生效配置
{retention}

## 语言风格生效配置
{style}
"""

    runtime_path.write_text(runtime, encoding="utf-8")
    print(f"refreshed: {runtime_path}")


if __name__ == "__main__":
    main()
