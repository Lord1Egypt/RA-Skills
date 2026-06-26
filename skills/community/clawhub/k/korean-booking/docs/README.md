# 文档目录

## clinics/
由 `scripts/generate-md.js` 自动生成的静态医院预约页面。

### 用途
- **SEO 优化**：为每个医院创建独立的静态页面，便于搜索引擎索引
- **知识库**：作为内部知识库，供客服或用户直接查阅
- **API 备用**：当动态服务不可用时，可回退到静态页面

### 生成方式
```bash
npm run generate
```

### 文件命名规则
`{医院ID}-{英文名小写连字符}.md`
- 示例：`0001-jd-skin-clinic.md`
- ID 为 hospitals.json 中的 id 字段，补零至4位

## superpowers/
预留目录，用于存放技能相关的增强文档或计划。

### plans/
技能开发计划、路线图等文档。