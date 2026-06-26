---
name: godot-shader
description: Godot 4.x shader development guide covering visual effects, materials, particle shaders, and optimization. Use when creating custom shaders, visual effects, post-processing, or optimizing rendering performance in Godot games. Includes shader templates and common effects.
---

# Godot 着色器开发指南

## 着色器基础

### 着色器类型
```yaml
Spatial (3D):
  - 3D 模型材质
  - 光照和阴影
  - 后处理效果

CanvasItem (2D):
  - 2D 精灵效果
  - UI 特效
  - 粒子系统

Particles:
  - GPU 粒子
  - 高性能粒子效果
```

### 基本结构
```glsl
shader_type canvas_item;

// 顶点着色器（可选）
void vertex() {
    VERTEX += vec2(sin(TIME), cos(TIME));
}

// 片段着色器
void fragment() {
    COLOR = texture(TEXTURE, UV);
}
```

## 常用 2D 效果

### 1. 发光效果
```glsl
shader_type canvas_item;

uniform float glow_intensity : hint_range(0, 10) = 2.0;
uniform vec4 glow_color : source_color = vec4(1.0, 1.0, 1.0, 1.0);

void fragment() {
    vec4 tex_color = texture(TEXTURE, UV);
    
    // 边缘检测
    vec2 size = TEXTURE_PIXEL_SIZE;
    float alpha = 0.0;
    alpha += texture(TEXTURE, UV + vec2(0.0, -size.y)).a;
    alpha += texture(TEXTURE, UV + vec2(0.0, size.y)).a;
    alpha += texture(TEXTURE, UV + vec2(-size.x, 0.0)).a;
    alpha += texture(TEXTURE, UV + vec2(size.x, 0.0)).a;
    alpha = max(0.0, alpha - tex_color.a * 4.0);
    
    COLOR = tex_color + glow_color * alpha * glow_intensity;
}
```

### 2. 波纹扭曲
```glsl
shader_type canvas_item;

uniform float wave_amplitude = 10.0;
uniform float wave_frequency = 5.0;
uniform float wave_speed = 2.0;

void fragment() {
    vec2 distorted_uv = UV;
    distorted_uv.x += sin(UV.y * wave_frequency + TIME * wave_speed) * wave_amplitude * 0.01;
    distorted_uv.y += cos(UV.x * wave_frequency + TIME * wave_speed) * wave_amplitude * 0.01;
    
    COLOR = texture(TEXTURE, distorted_uv);
}
```

### 3. 颜色替换
```glsl
shader_type canvas_item;

uniform vec4 old_color : source_color = vec4(1.0, 0.0, 0.0, 1.0);
uniform vec4 new_color : source_color = vec4(0.0, 1.0, 0.0, 1.0);
uniform float tolerance : hint_range(0, 1) = 0.1;

void fragment() {
    vec4 tex_color = texture(TEXTURE, UV);
    
    float dist = distance(tex_color.rgb, old_color.rgb);
    if (dist < tolerance) {
        COLOR = vec4(new_color.rgb, tex_color.a);
    } else {
        COLOR = tex_color;
    }
}
```

### 4. 溶解效果
```glsl
shader_type canvas_item;

uniform float dissolve_amount : hint_range(0, 1) = 0.5;
uniform sampler2D noise_texture;
uniform vec4 edge_color : source_color = vec4(1.0, 0.5, 0.0, 1.0);

void fragment() {
    vec4 tex_color = texture(TEXTURE, UV);
    float noise = texture(noise_texture, UV).r;
    
    if (noise < dissolve_amount) {
        discard; // 完全透明
    } else if (noise < dissolve_amount + 0.1) {
        COLOR = edge_color; // 边缘发光
    } else {
        COLOR = tex_color;
    }
}
```

### 5. 精灵闪烁
```glsl
shader_type canvas_item;

uniform float flash_speed = 5.0;
uniform float flash_intensity : hint_range(0, 1) = 0.5;

void fragment() {
    vec4 tex_color = texture(TEXTURE, UV);
    float flash = sin(TIME * flash_speed) * 0.5 + 0.5;
    tex_color.rgb += vec3(flash * flash_intensity);
    COLOR = tex_color;
}
```

## 3D 着色器

### PBR 材质
```glsl
shader_type spatial;

uniform vec4 albedo : source_color = vec4(1.0, 1.0, 1.0, 1.0);
uniform float metallic : hint_range(0, 1) = 0.0;
uniform float roughness : hint_range(0, 1) = 0.5;
uniform sampler2D albedo_texture;
uniform sampler2D normal_texture;

void fragment() {
    ALBEDO = albedo.rgb * texture(albedo_texture, UV).rgb;
    METALLIC = metallic;
    ROUGHNESS = roughness;
    NORMAL_MAP = texture(normal_texture, UV).rgb;
}
```

### 全息效果
```glsl
shader_type spatial;

uniform float scanline_speed = 2.0;
uniform float scanline_frequency = 50.0;
uniform vec4 hologram_color : source_color = vec4(0.0, 1.0, 1.0, 1.0);

void fragment() {
    // 扫描线
    float scanline = sin(UV.y * scanline_frequency + TIME * scanline_speed);
    scanline = smoothstep(0.0, 0.5, scanline);
    
    // 边缘发光
    float fresnel = pow(1.0 - dot(NORMAL, VIEW), 3.0);
    
    ALBEDO = hologram_color.rgb;
    ALPHA = (scanline * 0.3 + 0.7) * (fresnel + 0.3);
    EMISSION = hologram_color.rgb * fresnel * 2.0;
}
```

### 水面效果
```glsl
shader_type spatial;

uniform float wave_speed = 1.0;
uniform float wave_height = 0.5;
uniform sampler2D normal_map1;
uniform sampler2D normal_map2;

void vertex() {
    VERTEX.y += sin(VERTEX.x * 2.0 + TIME * wave_speed) * wave_height;
    VERTEX.y += cos(VERTEX.z * 2.0 + TIME * wave_speed * 0.8) * wave_height;
}

void fragment() {
    vec2 uv1 = UV * 1.0 + TIME * 0.05;
    vec2 uv2 = UV * 1.0 - TIME * 0.03;
    
    vec3 n1 = texture(normal_map1, uv1).rgb;
    vec3 n2 = texture(normal_map2, uv2).rgb;
    
    NORMAL_MAP = mix(n1, n2, 0.5);
    ALBEDO = vec3(0.1, 0.4, 0.8);
    METALLIC = 0.8;
    ROUGHNESS = 0.2;
}
```

## 粒子着色器

### 火焰粒子
```glsl
shader_type particles;

void start() {
    // 初始速度向上
    VELOCITY = vec3(randf_range(-1.0, 1.0), randf_range(2.0, 5.0), randf_range(-1.0, 1.0));
    
    // 随机大小
    float scale = randf_range(0.5, 1.5);
    TRANSFORM[0][0] *= scale;
    TRANSFORM[1][1] *= scale;
    TRANSFORM[2][2] *= scale;
    
    // 随机颜色（红到黄）
    COLOR.r = 1.0;
    COLOR.g = randf_range(0.0, 1.0);
    COLOR.b = 0.0;
}

void process() {
    // 逐渐变小
    float scale = 1.0 - LIFETIME / LIFETIME;
    TRANSFORM[0][0] *= scale;
    TRANSFORM[1][1] *= scale;
    
    // 逐渐透明
    COLOR.a = 1.0 - LIFETIME / LIFETIME;
}
```

### 魔法粒子
```glsl
shader_type particles;

uniform float orbit_radius = 2.0;
uniform float orbit_speed = 2.0;

void start() {
    COLOR = vec4(0.5, 0.0, 1.0, 1.0); // 紫色
    TRANSFORM[3].xyz = vec3(0.0, 0.0, 0.0); // 从中心开始
}

void process() {
    // 环绕运动
    float angle = LIFETIME * orbit_speed;
    TRANSFORM[3].x = cos(angle) * orbit_radius;
    TRANSFORM[3].z = sin(angle) * orbit_radius;
    
    // 闪烁
    COLOR.a = sin(LIFETIME * 10.0) * 0.5 + 0.5;
}
```

## 后处理效果

### 屏幕抖动
```glsl
shader_type canvas_item;

uniform float shake_intensity = 5.0;
uniform float shake_speed = 10.0;

void fragment() {
    vec2 shake = vec2(
        sin(TIME * shake_speed) * shake_intensity,
        cos(TIME * shake_speed * 1.3) * shake_intensity
    ) * 0.001;
    
    COLOR = texture(TEXTURE, UV + shake);
}
```

### 暗角效果
```glsl
shader_type canvas_item;

uniform float vignette_intensity : hint_range(0, 2) = 0.5;
uniform float vignette_radius : hint_range(0, 1) = 0.8;

void fragment() {
    vec4 tex_color = texture(TEXTURE, UV);
    
    vec2 center = UV - 0.5;
    float dist = length(center);
    float vignette = smoothstep(vignette_radius, 0.0, dist);
    
    tex_color.rgb *= mix(1.0 - vignette_intensity, 1.0, vignette);
    COLOR = tex_color;
}
```

### 色差效果
```glsl
shader_type canvas_item;

uniform float aberration_amount = 0.005;

void fragment() {
    vec2 direction = normalize(UV - 0.5);
    float r = texture(TEXTURE, UV + direction * aberration_amount).r;
    float g = texture(TEXTURE, UV).g;
    float b = texture(TEXTURE, UV - direction * aberration_amount).b;
    
    COLOR = vec4(r, g, b, 1.0);
}
```

## 性能优化

### 技巧
```yaml
1. 避免复杂计算:
   - 预计算常量
   - 使用 lowp/mediump 精度
   
2. 减少纹理采样:
   - 合并纹理到图集
   - 使用 mipmaps
   
3. 简化条件分支:
   - 使用 mix() 替代 if
   - 避免动态分支
   
4. 利用 GPU 并行:
   - 向量化计算
   - 避免依赖前一个像素
```

### 精度选择
```glsl
// 低精度（移动端）
uniform lowp vec4 color;

// 中精度（大多数情况）
uniform mediump float intensity;

// 高精度（需要精确计算）
uniform highp mat4 transform;
```

## 调试技巧

### 可视化法线
```glsl
void fragment() {
    ALBEDO = NORMAL * 0.5 + 0.5; // 法线可视化
}
```

### 可视化 UV
```glsl
void fragment() {
    ALBEDO = vec3(UV, 0.0); // UV 可视化
}
```

### 性能分析
```
# 使用 Godot 内置分析器
Debugger > Profiler > Start

# 查看 Draw Calls
Debugger > Monitors > 2D Draw Calls
```

## 参考资源

- **常用效果**: [references/common-effects.md](references/common-effects.md)
- **优化指南**: [references/optimization.md](references/optimization.md)
- **数学函数**: [references/math-functions.md](references/math-functions.md)
