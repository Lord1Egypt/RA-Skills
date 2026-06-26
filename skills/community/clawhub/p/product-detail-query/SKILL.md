---
name: 产品详情查询
description: 通过产品名称查询保险产品详细信息，支持自动匹配多个版本
version: 1.0.0
author: @wangbaiqi521
tags: 保险,产品查询,API调用
license: MIT-0
---

# 产品详情查询 Skill

## 任务目标
- 本 Skill 用于：根据产品名称查询产品的详细信息
- 能力包含：产品名称到参数映射、API 调用、结果返回
- 触发条件：用户输入产品名称询问详情、需要查看产品配置或规格

## 前置准备
- 无需额外依赖

## 操作步骤
- 标准流程：
  1. **接收产品名称**：用户输入产品名称，如"泰康百万药无忧D款（庆典版）医疗保险"或"平安e生保"
  2. **查找映射参数**：
     - 读取 `references/product-mapping.csv` 文件
     - 根据产品名称查找对应的 `productCode` 和 `secondTypeId`
     - CSV 格式：`productCode,productName,displayName,secondTypeId`
  3. **处理多个匹配结果**：
     - 如果找到多个匹配的产品（如"平安e生保"有计划一、计划二、计划三、计划四），选择第一个匹配结果进行查询
     - 向用户说明选择了哪个具体版本（如"平安e生保（悦享版）医疗保险（计划一）"）
  4. **调用查询接口**：
     - 执行 `scripts/main.py --product-code <productCode> --second-type-id <secondTypeId>`
     - 获取 API 返回的产品详情数据
  5. **返回结果**：将产品详情信息整理后返回给用户

## 资源索引
- 必要脚本：见 [scripts/main.py](scripts/main.py) (用途：调用产品详情 API，参数：product_code, second_type_id)
- 数据映射：见 [references/product-mapping.csv](references/product-mapping.csv) (何时读取：用户输入产品名称后查找参数)

## 注意事项
- 产品名称匹配时注意大小写和空格
- 如果找不到匹配的产品，提示用户确认产品名称
- API 调用失败时，检查网络连接和参数正确性
- 当输入的产品名称匹配到多个产品时，自动选择第一个匹配结果进行查询，并在返回结果中说明选择了哪个具体版本

## 使用示例
- 用户："查询泰康百万药无忧D款（庆典版）医疗保险的详细信息"
  - 在 CSV 中查找：productCode=dbt14396513981, secondTypeId=4
  - 执行：`scripts/main.py --product-code dbt14396513981 --second-type-id 4`
  - 返回产品详情数据

- 用户："查询平安e生保的详细信息"
  - 在 CSV 中找到多个匹配：计划一、计划二、计划三、计划四
  - 自动选择第一个：平安e生保（悦享版）医疗保险（计划四），productCode=dbp14485804100, secondTypeId=4
  - 执行：`scripts/main.py --product-code dbp14485804100 --second-type-id 4`
  - 返回产品详情数据，并说明："为您查询的是平安e生保（悦享版）医疗保险（计划四）的详细信息"
