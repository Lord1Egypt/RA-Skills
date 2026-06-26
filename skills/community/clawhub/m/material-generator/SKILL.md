# UE材质生成器技能包

## 部署地址（最新）
```
App:  https://k2lucelsen19.space.minimaxi.com
示例JSON（血迹后处理材质）: https://k2lucelsen19.space.minimaxi.com/BP_BloodPostProcess.json
```

## 项目位置
`/workspace/material-generator/`

## 概述
UE材质生成器：输入自然语言描述 → 生成UE材质节点图（支持TextureSample、Multiply、Lerp、Constant、TexCoord、MaterialOutput等节点）。

## 核心文件
- `src/App.tsx` — 主界面（输入框/历史/修改面板）
- `src/MaterialCanvas.tsx` — ReactFlow画布（拖拽节点）
- `src/BpNode.tsx` — 材质节点渲染（官方UE颜色）
- `src/Sidebar.tsx` — 选中节点信息/修改
- `src/api.ts` — AI生成逻辑 + autoLayout
- `src/types.ts` — MaterialGraph/MaterialNode/MaterialPin类型
- `public/` — 静态JSON示例文件

## API配置
- Base: `https://api.minimaxi.com/v1`
- Model: `MiniMax-M2.7`
- Key: `sk-cp-g2MZf43bhLucC0sCMI-BeaXycKl5MDj_dPN_mPKn7IfqlAL1bS8YP-ERiEi9ZJMLu7I2XXIMjw9Xb8x-9iONlnOg24dBV5imId_W5v1oyivKwZCMr7nix6c`

## 节点颜色（UE官方标准）
- texture_sample: header=#A855F7 紫色
- math: header=#00D4FF 青色
- lerp: header=#FBBF24 黄色
- param: header=#F97316 橙色
- constant: header=#22C55E 绿色
- output: header=#16A34A 深绿
- texcoord: header=#3B82F6 蓝色

## Pin颜色
- float: #22C55E
- float2: #00D4FF
- float3: #FBBF24
- float4: #F97316
- sampler: #A855F7

## 常见问题
- 构建失败：检查tsconfig.json是否包含必要配置
- Sidebar.tsx中JSX字符串必须用双引号，避免嵌套引号问题
- 删除残留的BlueprintCanvas.tsx（从蓝图生成器复制时会带过来）
