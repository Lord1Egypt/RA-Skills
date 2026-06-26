#!/bin/bash
# 初始化原型工作区
# 用法: bash init-workspace.sh <目标目录> <skill根目录>

TARGET_DIR="$1"
SKILL_DIR="$2"
TEMPLATE_DIR="$SKILL_DIR/template-project"

if [ -z "$TARGET_DIR" ] || [ -z "$SKILL_DIR" ]; then
  echo "用法: bash init-workspace.sh <目标目录> <skill根目录>"
  exit 1
fi

# 如果目标目录不存在，从模板复制
if [ ! -f "$TARGET_DIR/package.json" ]; then
  echo "📦 从模板初始化工程..."
  mkdir -p "$TARGET_DIR"
  rsync -a --exclude='node_modules' --exclude='dist' "$TEMPLATE_DIR/" "$TARGET_DIR/"

  # 生成 skill 市场不接受的 .vue 文件
  mkdir -p "$TARGET_DIR/src/views"
  mkdir -p "$TARGET_DIR/src/layouts"

  cat > "$TARGET_DIR/src/App.vue" << 'APPEOF'
<template>
  <MainLayout>
    <router-view />
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from './layouts/MainLayout.vue'
</script>

<style>
#app { width: 100%; height: 100vh; }
</style>
APPEOF

  cat > "$TARGET_DIR/src/views/PlaceholderPage.vue" << 'PHEOF'
<template>
  <div style="display: flex; align-items: center; justify-content: center; height: 100%; color: var(--color-text-3);">
    <a-empty description="等待页面生成..." />
  </div>
</template>
PHEOF
fi

# 如果没有 node_modules，执行 npm install
if [ ! -d "$TARGET_DIR/node_modules" ]; then
  echo "📥 安装依赖（首次需要，后续跳过）..."
  cd "$TARGET_DIR" && npm install --silent
else
  echo "✅ 依赖已存在，跳过安装"
fi

echo "✅ 工作区就绪: $TARGET_DIR"
