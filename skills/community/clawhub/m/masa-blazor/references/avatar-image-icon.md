# 图片与图标

## MAvatar 头像

文档: https://docs.masastack.com/blazor/ui-components/avatars

### 基础用法
```razor
<MAvatar>
    <MImage Src="avatar.jpg" />
</MAvatar>

<MAvatar Color="primary">
    <span class="white--text text-h5">JD</span>
</MAvatar>

<MAvatar Color="teal">
    <MIcon Dark>mdi-account</MIcon>
</MAvatar>
```

### 尺寸
```razor
<MAvatar Size="32"><MImage Src="avatar.jpg" /></MAvatar>
<MAvatar Size="48"><MImage Src="avatar.jpg" /></MAvatar>
<MAvatar Size="64"><MImage Src="avatar.jpg" /></MAvatar>
<MAvatar Size="128"><MImage Src="avatar.jpg" /></MAvatar>
```

### 头像组
```razor
<MAvatarGroup Max="3">
    <MAvatar><MImage Src="user1.jpg" /></MAvatar>
    <MAvatar><MImage Src="user2.jpg" /></MAvatar>
    <MAvatar><MImage Src="user3.jpg" /></MAvatar>
    <MAvatar><MImage Src="user4.jpg" /></MAvatar>
    <MAvatar><MImage Src="user5.jpg" /></MAvatar>
</MAvatarGroup>
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Size | Int/String | 尺寸(px) |
| Color | String | 背景色 |
| Tile | Boolean | 直角(无圆角) |
| Rounded | Boolean/String | 圆角 |
| Left | Boolean | 左对齐 |
| Right | Boolean | 右对齐 |
| Dark | Boolean | 暗色文字 |
| Light | Boolean | 亮色文字 |

---

## MImage 图片

文档: https://docs.masastack.com/blazor/ui-components/images

### 基础用法
```razor
<MImage Src="image.jpg" Alt="图片描述" />
```

### 响应式图片
```razor
<MImage Src="image.jpg" MaxWidth="400" MaxHeight="300" Contain />
```

### 懒加载
```razor
<MImage Src="image.jpg" LazySrc="placeholder.jpg" Height="300" />
```

### Aspect Ratio
```razor
<MImage Src="image.jpg" AspectRatio="16/9" />
<MImage Src="image.jpg" AspectRatio="1" /> <!-- 正方形 -->
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Src | String | 图片URL |
| LazySrc | String | 懒加载占位图 |
| Alt | String | 替代文本 |
| AspectRatio | Double/String | 宽高比 |
| Width | Int/String | 宽度 |
| Height | Int/String | 高度 |
| MaxWidth | Int/String | 最大宽度 |
| MaxHeight | Int/String | 最大高度 |
| MinWidth | Int/String | 最小宽度 |
| MinHeight | Int/String | 最小高度 |
| Contain | Boolean | 包含模式(不裁剪) |
| Cover | Boolean | 覆盖模式(裁剪) |
| Gradient | String | 渐变遮罩 |
| Position | String | 图片位置 |
| Transition | String | 过渡动画 |
| Eager | Boolean | 立即加载 |
| Sizes | String | 响应式尺寸 |
| Srcset | String | 响应式图片集 |

---

## MIcon 图标

文档: https://docs.masastack.com/blazor/ui-components/icons

### 基础用法
```razor
<MIcon>mdi-home</MIcon>
<MIcon>mdi-account</MIcon>
<MIcon>mdi-settings</MIcon>
```

### 带颜色和尺寸
```razor
<MIcon Color="primary" Size="24">mdi-star</MIcon>
<MIcon Color="red" Size="32">mdi-heart</MIcon>
<MIcon Color="green" Size="48">mdi-check-circle</MIcon>
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Size | Int/String | 尺寸(px) |
| Color | String | 颜色 |
| Dark | Boolean | 暗色 |
| Light | Boolean | 亮色 |
| Dense | Boolean | 紧凑 |
| Left | Boolean | 左侧(用于文字前) |
| Right | Boolean | 右侧(用于文字后) |
| XSmall | Boolean | 超小 |
| Small | Boolean | 小 |
| Medium | Boolean | 中 |
| Large | Boolean | 大 |
| XLarge | Boolean | 超大 |

### 支持的图标库
- **Material Design Icons (mdi)**: 默认图标库
  - 前缀: `mdi-` + 图标名
  - 示例: `mdi-home`, `mdi-account`, `mdi-settings`
  - 完整列表: https://pictogrammers.github.io/@mdi/font/7.4.47/


## 事件
### MAvatar
| 事件 | 说明 |
|------|------|
| OnClick | 点击时触发 |

### MImage
| 事件 | 说明 |
|------|------|
| OnLoad | 图片加载完成时触发 |
| OnError | 图片加载失败时触发 |

### MIcon
| 事件 | 说明 |
|------|------|
| OnClick | 点击时触发 |