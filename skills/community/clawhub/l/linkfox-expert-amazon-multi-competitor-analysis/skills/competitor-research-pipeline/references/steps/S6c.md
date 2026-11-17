# S6c: A+内容与商品图对比分析（独立模块，需AIGC）

> 与S6/S6b/S7并行执行。基于Amazon Product Detail返回的A+内容和商品图片URL，通过AIGC多模态模型做视觉对比分析，输出目标ASIN的A+优化方案和商品图优化方案。

## 输入
- product_details: S2已拉取的Amazon Product Detail数据
  - `productDescription`: A+内容JSON（含模块图片URL和标题）
  - `productImageUrls`: 商品图片URL列表（主图+副图）
  - `thumbnail`: 缩略图URL
  - `aboutItemFivePoint`: 五点描述（卖点参考）
- target_asin + competitors: S1竞品名单
- target_features: S0提取的目标特征清单

## 依赖
S2（需要Amazon Product Detail数据）

## 操作

### Part A: A+内容对比分析

**Step 1: 提取A+模块清单**
- 从每个ASIN的`productDescription`中解析A+模块
- 记录每个模块的: 图片URL、标题、位置顺序
- 统计: 模块数量、模块类型推测（对比表/场景图/功能图解/品牌故事/使用教程）

**Step 2: AIGC逐ASIN分析A+图片（GEM_3_FLASH）**
- 每次传入1个ASIN的全部A+图片URL（最多10张）
- prompt:
```
你是亚马逊A+页面分析专家。请分析这些A+页面图片，识别：
1. 每张图的模块类型(对比表/场景图/功能图解/品牌故事/使用教程/FAQ)
2. 卖点优先级(第一屏强调什么功能/卖点)
3. 视觉策略(实拍/渲染/信息图/混合)
4. 使用场景展示(运动/通勤/居家/儿童/办公)
5. 转化钩子(限时/赠品/对比/FAQ/赠品/套装)
6. 文字密度(高/中/低)
7. 品牌一致性(强/中/弱)
输出JSON数组，每张图一个对象。
```

**Step 3: A+横向对比**
- 模块结构对比：每个竞品几屏、每屏什么类型
- 卖点优先级矩阵：各ASIN第一屏→最后一屏的卖点排序
- 视觉策略分布：实拍型/信息图型/混合型
- 场景覆盖热力图：哪些场景被覆盖、哪些被忽略
- 转化钩子使用率：对比表/FAQ/赠品展示的使用比例

**Step 4: 提取亮点和不足**
- 每个竞品A+的最大亮点（如：对比表设计优秀/场景图拍摄专业/信息图逻辑清晰）
- 每个竞品A+的明显不足（如：文字过多/缺少使用场景/无对比表/品牌感弱）

### Part B: 商品图片对比分析

**Step 1: 提取商品图片清单**
- 从`productImageUrls`获取每个ASIN的全部商品图片URL
- 记录: 图片数量、图片顺序

**Step 2: AIGC逐ASIN分析商品图片（GEM_3_FLASH）**
- 主图分析: 构图/角度/背景/文字叠加/产品占比
- 副图分析: 类型分布(场景图/功能图/尺寸图/对比图/包装图)
- prompt:
```
你是亚马逊商品图分析专家。请分析这些商品图片：
图1是主图，图2-N是副图。对每张图识别：
1. 图片类型(白底主图/场景图/功能图解/尺寸图/对比图/包装图/生活方式图)
2. 构图(居中/对角线/三分法)
3. 产品占比(高/中/低)
4. 文字叠加(有/无，如有则提取文字内容)
5. 卖点表达(这张图在强调什么功能/场景)
6. 视觉质量(专业/中等/业余)
输出JSON数组。
```

**Step 3: 商品图横向对比**
- 主图策略对比: 白底/场景/角度/文字
- 副图数量对比: 谁用了更多图片位
- 副图类型分布: 场景图/功能图/尺寸图/对比图的比例
- 卖点可视化覆盖: 哪些卖点被图片化、哪些没有
- 信息图使用率: 有多少ASIN使用了文字标注的信息图

### Part C: 综合优化方案

**Step 1: 吸取优点**
- 从所有竞品A+中提取最值得借鉴的模块设计
- 从所有竞品商品图中提取最有效的图片策略

**Step 2: 规避缺点**
- 列出所有竞品共性的不足（避免犯同样错误）
- 列出目标ASIN当前A+和图片的明显短板

**Step 3: 输出目标ASIN优化方案**
- A+模块结构建议（推荐几屏、每屏什么类型、卖点排序）
- A+视觉策略建议（实拍/信息图/混合、场景覆盖建议）
- 商品图策略建议（主图改进、副图补充、信息图设计）
- 参考素材清单（哪些竞品的哪些图可以直接参考风格）

## 输出
```json
{
  "aplus_analysis": {
    "per_asin": {
      "asin": {
        "module_count": N,
        "modules": [{"type": "", "first_focus": "", "visual": "", "scenes": [], "hooks": []}],
        "strengths": [],
        "weaknesses": []
      }
    },
    "comparison": {
      "module_structure": {},
      "selling_point_order": {},
      "visual_strategy": {},
      "scene_coverage": {},
      "conversion_hooks": {}
    }
  },
  "image_analysis": {
    "per_asin": {
      "asin": {
        "image_count": N,
        "main_image": {"composition": "", "background": "", "text_overlay": "", "product_ratio": ""},
        "secondary_images": [{"type": "", "selling_point": "", "quality": ""}],
        "strengths": [],
        "weaknesses": []
      }
    },
    "comparison": {
      "main_image_strategy": {},
      "image_count_ranking": [],
      "type_distribution": {},
      "infographic_usage": {}
    }
  },
  "optimization_plan": {
    "aplus_recommendation": {
      "module_structure": [],
      "selling_point_order": [],
      "visual_strategy": "",
      "scene_coverage": [],
      "avoid": []
    },
    "image_recommendation": {
      "main_image": "",
      "secondary_images": [],
      "infographic_design": "",
      "missing_visualization": []
    },
    "reference_materials": [{"competitor_asin": "", "reference_type": "", "reason": ""}]
  }
}
```

## 用途
被S8(SWOT研判：机会维度"视觉优化空间")消费
被S9(报告：A+与商品图章节)消费
可独立交付给图片生成Skill(linkfox-aigc-imagegen-product)作为生成依据
