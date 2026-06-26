# image-scanner-pro

## Description
扫描图片文件夹，调用视觉大模型（Gemini 2.0 Flash）深度分析每张照片的摄影属性：景别、主体、场景、光线、氛围、影调、产品、物件、陈设。

## Triggers
- 分析摄影作品
- 识别图片内容
- 扫描并分类图片
- 批量分析照片风格
- 整理作品集
- 识别图片颜色和风格

## Capabilities
- 扫描目录中的所有图片文件
- 调用视觉模型分析每张图片
- 识别专业摄影属性（景别/主体/光线/影调等）
- 按拍摄内容自动分类
- 生成详细分析报告
- 支持批量处理

## Requirements
- 需要配置视觉模型 API（Gemini 2.0 Flash）
- 安装依赖：npm install @google/generative-ai

## Usage
```bash
node skills/image-scanner-pro/index.js --path <目录路径> --api-key <Gemini Key> --output report.json