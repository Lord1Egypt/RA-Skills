---
name: gpu-shader-toolkit
description: Expert GPU shader development toolkit covering HLSL, GLSL, MSL, WGSL, ReShade FX, Unity ShaderLab, and WebGL. Features cross-language conversion, GPU performance optimization, noise/lighting functions, platform gotchas, debugging, production-ready templates, NVIDIA shader cache analysis with nvcachetools/nvdisasm/envytools for compiled shader reverse engineering, DirectX shader decompilation, game shader PAK file reverse engineering and DXBC disassembly for extracting compiled shaders from game archives (Warframe/EvoEngine-style), PSP/PPSSPP GE dump (.ppdmp) analysis for extracting generated shaders from PSP games, and advanced performance optimization based on compiled shader analysis.
---

# GPU Shader Toolkit

Expert-level GPU shader development, optimization, reverse engineering, and conversion across all major shader languages and platforms.

---

## Quick Reference

### Language Detection (One Glance)

| Pattern | Language |
|---------|----------|
| `SV_Position`, `cbuffer`, `register(b0)` | HLSL |
| `gl_Position`, `uniform`, `layout(binding=)` | GLSL |
| `[[position]]`, `[[buffer(0)]]`, `metal_stdlib` | MSL |
| `@vertex`, `@fragment`, `@binding(0)` | WGSL |
| `technique`, `pass`, `tex2D(`, `ui_type=` | ReShade FX |
| `Shader "..."`, `Properties`, `SubShader` | Unity ShaderLab |
| `attribute`, `varying`, `precision mediump` | GLSL ES 1.00 (WebGL 1) |
| `in`, `out`, `layout(location=)`, `#version 300` | GLSL ES 3.00 (WebGL 2) |

### Type Quick Reference

| HLSL | GLSL | MSL | WGSL |
|------|------|-----|------|
| `float2` | `vec2` | `float2` | `vec2<f32>` |
| `float3` | `vec3` | `float3` | `vec3<f32>` |
| `float4` | `vec4` | `float4` | `vec4<f32>` |
| `float3x3` | `mat3` | `float3x3` | `mat3x3<f32>` |
| `float4x4` | `mat4` | `float4x4` | `mat4x4<f32>` |

### Function Quick Reference

| Operation | HLSL | GLSL |
|-----------|------|------|
| Fractional | `frac(x)` | `fract(x)` |
| Lerp | `lerp(a,b,t)` | `mix(a,b,t)` |
| Saturate | `saturate(x)` | `clamp(x,0,1)` |
| Mod | `fmod(a,b)` | `mod(a,b)` |
| Texture | `tex.Sample(s,uv)` | `texture(tex,uv)` |
| DDX | `ddx(x)` | `dFdx(x)` |

### Performance Critical Patterns

```hlsl
// ALWAYS use sincos instead of separate sin/cos
float s, c; sincos(angle, s, c);  // NOT: s=sin(a); c=cos(a);

// ALWAYS use multiply instead of pow for integers
float x2 = x * x;    // NOT: pow(x, 2.0)
float x3 = x * x * x; // NOT: pow(x, 3.0)

// ALWAYS use saturate instead of clamp to 0-1
float x = saturate(x);  // NOT: clamp(x, 0.0, 1.0)

// ALWAYS use dot for squared length
float lenSq = dot(v, v);  // NOT: length(v) * length(v)
```

---

## Supported Languages

| Language | Platform | Extensions |
|----------|----------|------------|
| HLSL | DirectX, Unity, Unreal | `.hlsl`, `.fx`, `.hlsli` |
| GLSL | OpenGL, Vulkan, WebGL | `.glsl`, `.vert`, `.frag`, `.comp`, `.geom` |
| MSL | Metal (Apple/iOS/macOS) | `.metal` |
| WGSL | WebGPU | `.wgsl` |
| ReShade FX | ReShade Post-Processing | `.fx` |
| ShaderLab | Unity Shaders | `.shader` |
| GLSL ES | WebGL 1.0/2.0 | `.glsl`, embedded |

---

## Shader Cache Reverse Engineering (NVIDIA)

### Overview

This section covers extracting and analyzing compiled NVIDIA GPU shaders from the driver's shader cache. This enables performance optimization, debugging, and understanding how your GLSL/HLSL code compiles to GPU assembly.

### Tools Required

| Tool | Purpose | Source |
|------|---------|--------|
| **nvcachetools** | Extract compiled shaders from NVIDIA cache | [github.com/therontarigo/nvcachetools](https://github.com/therontarigo/nvcachetools) |
| **nvdisasm** | NVIDIA proprietary disassembler | CUDA Toolkit or [standalone](https://developer.download.nvidia.com/compute/cuda/repos/) |
| **envytools** | Open-source NVIDIA disassembler | [github.com/envytools/envytools](https://github.com/envytools/envytools/) |
| **dx-shader-decompiler** | DirectX 9 shader decompiler | [github.com/aizvorski/dx-shader-decompiler](https://github.com/aizvorski/dx-shader-decompiler) |

---

### NVIDIA Shader Cache Workflow

#### Step 1: Enable and Locate Shader Cache

```bash
# Default cache locations
# Linux:   ~/.nv/GLCache/
# Windows: %LOCALAPPDATA%\NVIDIA\GLCache\

# Ensure cache directory exists
mkdir -p ~/.nv/GLCache

# Or set custom cache path
export __GL_SHADER_DISK_CACHE_PATH=/path/to/cache
```

**Important**: The cache directory may not exist by default. Create it manually or the driver won't save shader caches.

#### Step 2: Build nvcachetools

```bash
git clone https://github.com/therontarigo/nvcachetools.git
cd nvcachetools

# Build nvcachedec (extracts .toc/.bin to .nvuc files)
gcc -o nvcachedec nvcachedec.c

# Build nvucdump (extracts sections from .nvuc files)
gcc -o nvucdump nvucdump.c
```

#### Step 3: Extract Compiled Shaders

```bash
# Extract shaders from cache TOC file
# Creates object00000.nvuc, object00001.nvuc, etc.
./nvcachedec path/to/cache/*.toc output_objs/

# Extract sections from NVUC files
# Creates section4_0001.bin, etc.
./nvucdump output_objs/object00000.nvuc sections/
```

#### Step 4: Disassemble with nvdisasm

```bash
# Using NVIDIA's proprietary disassembler
# SM architecture codes:
# SM50 - Maxwell (GTX 750, 900 series)
# SM60 - Pascal (GTX 1000 series)
# SM70 - Volta
# SM75 - Turing (GTX 1600, RTX 2000 series)
# SM80 - Ampere (RTX 3000 series)
# SM89 - Ada Lovelace (RTX 4000 series)

nvdisasm --binary SM89 output_objs/object00000.nvuc
nvdisasm --binary SM75 output_objs/object00000.nvuc
```

#### Step 5: Disassemble with envytools (Open Source)

```bash
# Using open-source envydis
# -i: interactive mode
# -mgm107: Maxwell GM107 architecture
./envydis -i -mgm107 sections/section4_0001.bin
```

---

### Analyzing Compiled Shader Output

#### Instruction Count Statistics

```bash
# Count instruction frequency in compiled shader
nvdisasm --print-code --binary SM87 object.nvuc | \
  sed '1d' | \
  sed -e 's/@[!|A-Za-z0-9]* / /g' | \
  perl -p0 -e 's#/\*.*?\*/##sg' | \
  sed "s/^[{|}| \t]*//" | \
  sed 's/\s.*$//' | \
  sort | uniq -c
```

#### Key Performance Instructions

| Instruction | Meaning | Performance Impact |
|-------------|---------|-------------------|
| **STL** | Store to Local Memory | **HIGH** - Often indicates array usage slowdown |
| **LDL** | Load from Local Memory | HIGH - Paired with STL, memory access |
| **FFMA_FP32** | Fused Multiply-Add | Medium - Basic math operation |
| **FMUL/FADD** | Multiply/Add | Low - Simple ALU operations |
| **MUFU.SIN/COS** | Transcendental sin/cos | High - Expensive operations |
| **TEX** | Texture sampling | Variable - Depends on cache hits |

---

### NVIDIA-Specific Optimization Insights

#### STL (Store to Local Memory) Optimization

**Problem**: NVIDIA OpenGL compiler can generate excessive STL instructions when using arrays, causing major slowdowns.

**Symptoms**:
- Shader runs slowly in OpenGL but fast in Vulkan
- Large arrays (especially `int[200+]`) trigger STL explosions
- Array copies as function arguments cause STL chains

**Solutions**:

```glsl
// BEFORE: Large int array - causes STL explosion
int map[220];  // Each element stored to local memory
for(int i=0; i<220; i++) map[i] = 0;

// AFTER: Packed into uint array - much smaller
uint map[7];   // 7 * 32 = 224 bits, enough for 220 flags
for(int i=0; i<7; i++) map[i] = 0u;

// Bit access functions
bool getBit(uint map[7], int index) {
    return (map[index/32] & (1u << (index%32))) != 0u;
}
void setBit(inout uint map[7], int index) {
    map[index/32] |= (1u << (index%32));
}
```

#### CONST (Constants) Memory Optimization

**Problem**: Too many unique float constants can degrade performance significantly.

**Guideline**: Keep constant data under **1-2 KB** for optimal performance on most NVIDIA GPUs.

```glsl
// BEFORE: Many unique floats (slow)
const mat4 weights[64] = mat4[64](
    mat4(0.01234, 0.05678, 0.09123, ...),
    mat4(0.03456, 0.07890, 0.01234, ...),
    // ... many unique values
);

// AFTER: Quantized floats (faster, minor quality loss)
// Round floats to fewer unique values
const mat4 weights[64] = mat4[64](
    mat4(0.012, 0.057, 0.091, ...),  // Rounded to ~1/100 precision
    mat4(0.035, 0.079, 0.012, ...),
    // ... fewer unique values = less CONST memory
);
```

**Quantization Script** (Python):

```python
# cfloats.py - Quantize float constants
def quantize_floats(floats, scale=132.0):
    """Reduce unique floats by quantizing to scale bins"""
    return [round(f * scale) / scale for f in floats]

# Example: 0.011, 0.012, 0.0115 -> all become 0.011 with scale=132
```

---

### OpenGL vs Vulkan Compiler Differences

NVIDIA's OpenGL and Vulkan shaders can compile differently:

```bash
# Compare same shader compiled in OpenGL vs Vulkan
# OpenGL cache location
~/.nv/GLCache/<hash>/nvcache.toc

# Run application with OpenGL, extract
nvcachedec opengl_cache/*.toc ogl_objs/

# Run same application with Vulkan, extract  
nvcachedec vulkan_cache/*.toc vk_objs/

# Compare instruction counts
nvdisasm --print-code --binary SM87 ogl_objs/object00000.nvuc | wc -l
nvdisasm --print-code --binary SM87 vk_objs/object00000.nvuc | wc -l
```

**Common Findings**:
- Vulkan compiler (via glslangValidator) often optimizes better
- OpenGL-only STL slowdowns may not appear in Vulkan
- Same GLSL can produce very different assembly

---

### Shader Architecture Reference (SM Codes)

| Architecture | SM Code | GPUs | Year |
|--------------|---------|------|------|
| Maxwell | SM50/SM52 | GTX 750, 900 series | 2014 |
| Pascal | SM60/SM61 | GTX 1000 series | 2016 |
| Volta | SM70 | Titan V, V100 | 2017 |
| Turing | SM75 | RTX 2000, GTX 1600 | 2018 |
| Ampere | SM80/SM86 | RTX 3000, A100 | 2020 |
| Ada Lovelace | SM89 | RTX 4000 series | 2022 |

---

### Troubleshooting NVIDIA Shader Cache

#### Driver Version Changes (550+)

```bash
# Nvidia 550+ drivers changed binary format for Vulkan shaders
# Check if extraction fails
nvcachedec cache/*.toc output/
# If OpenGL shaders work but Vulkan don't, check:
# https://github.com/therontarigo/nvcachetools/issues/1
```

#### Cache Not Being Created

```bash
# Ensure cache directory exists
mkdir -p ~/.nv/GLCache

# Enable shader cache in NVIDIA settings
nvidia-settings -a ShaderCacheSize=10

# Or via environment
export __GL_SHADER_DISK_CACHE=1
export __GL_SHADER_DISK_CACHE_PATH=~/.nv/GLCache
```

#### Browser Cache (Encrypted)

Chrome and other browsers encrypt their shader caches, making them unusable with nvcachetools. Use minimal launchers instead:

- **Vulkan**: [vulkan-shadertoy-launcher](https://github.com/danilw/vulkan-shadertoy-launcher)
- **OpenGL**: Custom minimal OpenGL context

---

## DirectX Shader Decompilation

### DX9 Shader Decompilation

For DirectX 9 pixel/vertex shaders (SM 3.0):

```bash
# Get the tool
git clone https://github.com/aizvorski/dx-shader-decompiler.git
cd dx-shader-decompiler

# Decompile DX9 shader binary
python dx-shader-decompiler.py shader.bin

# Output: HLSL-like decompiled code
```

**Supported Formats**:
- Pixel Shader 3.0 (ps_3_0)
- Vertex Shader 3.0 (vs_3_0)

### DX10/11/12 Shader Analysis

For modern DirectX shaders (SM 4.0+):

```bash
# Use Microsoft's DirectX Shader Compiler (DXC) disassembler
dxc -dumpbin shader.dxil -Fc output.txt

# Or use AMD's RDNA shader analyzer
# Or use RenderDoc for runtime capture
```

---

## PSP/PPSSPP Shader Analysis

### Important: PSP Games Don't Have Traditional Shaders

**Critical Understanding**: PSP games use a fixed-function graphics pipeline with a programmable GPU called the "Graphics Engine" (GE). They do NOT contain shader code. Instead, PSP games use:
- **GE command lists** (display lists)
- **Fixed-function rendering states** (lighting, texturing, blending)
- **Transform matrices** and vertex processing

PPSSPP **generates shaders at runtime** by translating PSP GE commands into modern GLSL/HLSL/SPIR-V based on the current rendering state.

---

### PPSSPP Dump Files

| File Type | Location | Contents | Use Case |
|-----------|----------|----------|----------|
| `.ppdmp` | `SYSTEM/DUMP/` | GE frame dump (raw GE commands) | **Primary analysis target** |
| `.glshadercache` | `SYSTEM/CACHE/` | Compiled OpenGL shaders | Not useful - compiled |
| `.vkshadercache` | `SYSTEM/CACHE/` | Compiled Vulkan shaders | Not useful - compiled |

**Note**: Use `.ppdmp` files for shader analysis, NOT the compiled shader caches.

---

### Creating .ppdmp Frame Dumps

1. **Open PPSSPP** and load your game
2. Go to **Debug → GE debugger...** (Desktop versions only)
3. When the scene you want to capture is visible, click **"Record"** in the top right
4. After ~1 second, click **"Stop"**
5. Save the **.ppdmp** file to `SYSTEM/DUMP/`

**Wiki Reference**: https://github.com/hrydgard/ppsspp/wiki/How-to-create-a-frame-dump

---

### .ppdmp File Format Structure

#### Header (24 bytes)
```cpp
struct Header {
    char magic[8];        // "PPSSPPGE"
    uint32_t version;     // Current version: 6
    char gameID[9];       // Game disc ID (e.g., "ULUS12345")
    uint8_t pad[3];       // Padding
};
```

#### Version History
| Version | Features |
|---------|----------|
| 1 | Uncompressed (deprecated) |
| 2 | Snappy compression (minimum supported) |
| 3 | Adds FRAMEBUF0-FRAMEBUF9 |
| 4 | Expanded header with game ID |
| 5 | zstd compression (current) |
| 6 | Corrects dirty VRAM flag |

#### Command Types
```cpp
enum class CommandType : u8 {
    INIT = 0,           // Initial GPU state (512 * 4 bytes)
    REGISTERS = 1,      // GE register commands
    VERTICES = 2,       // Vertex data
    INDICES = 3,        // Index data
    CLUT = 4,           // Color Lookup Table data
    TRANSFERSRC = 5,    // Transfer source data
    TEXTURE0 = 0x10,    // Texture level 0-7 data
    FRAMEBUF0 = 0x18,   // Framebuffer data
    // ... etc
};
```

#### File Layout
```
[Header: 24 bytes]
[Command Count: 4 bytes]
[Push Buffer Size: 4 bytes]
[Compressed Commands Array: zstd]
[Compressed Push Buffer: zstd]
```

---

### Extracting Shader Information from .ppdmp

**Key Insight**: Shaders are NOT stored in .ppdmp files. They are **regenerated** from GE state during playback.

#### Workflow to Extract Generated Shaders

1. **Parse .ppdmp file**:
   - Validate magic = "PPSSPPGE"
   - Decompress commands and push buffer using zstd
   - Process INIT command for initial GPU state

2. **Reconstruct GPU State**:
   - INIT command contains 512 bytes of GE register state
   - REGISTERS commands update state during playback

3. **Compute Shader IDs**:
   - `ComputeVertexShaderID()` creates 64-bit ID from GE state
   - `ComputeFragmentShaderID()` creates fragment shader ID

4. **Generate Shader Code**:
   - `GenerateVertexShader()` produces GLSL/HLSL
   - `GenerateFragmentShader()` produces fragment shader

#### Key Shader ID Bits

**Vertex Shader Bits**:
| Bit | Meaning |
|-----|---------|
| `VS_BIT_IS_THROUGH` | Through mode (no transform) |
| `VS_BIT_USE_HW_TRANSFORM` | Hardware transform |
| `VS_BIT_LIGHTING_ENABLE` | Lighting enabled |
| `VS_BIT_HAS_NORMAL` | Has normal vectors |
| `VS_BIT_UVGEN_MODE` | UV generation mode |
| Bone/skinning weights | Up to 8 bones |

**Fragment Shader Bits**:
| Bit | Meaning |
|-----|---------|
| `FS_BIT_CLEARMODE` | Clear mode |
| `FS_BIT_DO_TEXTURE` | Texturing enabled |
| `FS_BIT_ALPHA_TEST` | Alpha test |
| `FS_BIT_COLOR_TEST` | Color test |
| Blend modes | Various blend functions |

---

### PPSSPP Source Code Reference

| File | Purpose |
|------|---------|
| `GPU/Debugger/RecordFormat.h` | File format structures |
| `GPU/Debugger/Record.cpp` | Recording implementation |
| `GPU/Debugger/Playback.cpp` | Playback/replay |
| `GPU/Common/ShaderId.cpp` | Shader ID computation |
| `GPU/Common/VertexShaderGenerator.cpp` | Vertex shader generation |
| `GPU/Common/FragmentShaderGenerator.cpp` | Fragment shader generation |
| `GPU/GPUState.h` | GE state structures |
| `GPU/ge_constants.h` | GE command constants |

---

### Parsing .ppdmp Example (C++)

```cpp
#include <zstd.h>
#include "GPU/Debugger/RecordFormat.h"

bool ParsePPDMP(const char* filename) {
    FILE* fp = fopen(filename, "rb");

    // Read header
    GPURecord::Header header;
    fread(&header, sizeof(header), 1, fp);

    if (memcmp(header.magic, "PPSSPPGE", 8) != 0) return false;
    if (header.version < 2 || header.version > 6) return false;

    // Read sizes
    uint32_t cmdCount, bufSize;
    fread(&cmdCount, sizeof(cmdCount), 1, fp);
    fread(&bufSize, sizeof(bufSize), 1, fp);

    // Read and decompress commands
    uint32_t compressedSize;
    fread(&compressedSize, sizeof(compressedSize), 1, fp);
    uint8_t* compressed = new uint8_t[compressedSize];
    fread(compressed, compressedSize, 1, fp);

    std::vector<GPURecord::Command> commands(cmdCount);
    ZSTD_decompress(commands.data(), cmdCount * sizeof(GPURecord::Command),
                    compressed, compressedSize);

    // Process commands
    for (const auto& cmd : commands) {
        switch (cmd.type) {
            case GPURecord::CommandType::INIT:
                // Initial GE state - 512 * 4 bytes of registers
                break;
            case GPURecord::CommandType::REGISTERS:
                // GE command list
                break;
            // ... handle other types
        }
    }
    return true;
}
```

---

### Tools for PSP Shader Analysis

| Tool | Purpose |
|------|---------|
| **PPSSPP GE Debugger** | Built-in frame analysis (Debug menu) |
| **PPSSPP Shader Viewer** | View generated shaders in developer tools |
| **RenderDoc** | Capture PPSSPP's Vulkan/D3D output |
| **Custom Parser** | Parse .ppdmp for batch analysis |

### Summary: PSP Shader Extraction

| What You Want | How To Get It |
|---------------|---------------|
| Game's rendering commands | GE Frame Dump (.ppdmp file) |
| PPSSPP's generated shaders | Use GE Debugger or parse dump |
| Understand shader generation | Read ShaderGenerator.cpp files |
| Debug graphics issues | GE Debugger (Debug menu) |

---

## Game Shader PAK File Extraction

### Overview

Many games ship compiled shaders in proprietary `.pak` archive files. This section covers reverse-engineering the PAK file format, extracting embedded shader binaries, and disassembling the contained DXBC (DirectX Bytecode) back into readable assembly. The methodology below was developed through actual extraction of 678 DX11 shaders from a Warframe `_wfshadersdx11.pak` file and is applicable to any game using similar archive patterns.

### When to Use This

- You have a `.pak`, `.package`, `.bundle`, or similar game archive containing compiled shaders
- You want to understand a game's rendering techniques by examining its shaders
- You need to extract shader bytecode for further analysis with external tools (DXC, RenderDoc)
- You're doing modding work and need to understand shader resource bindings

### General Approach: Format Reverse Engineering

**Step 1: File Identification**

Before writing any code, examine the file with hex tools to understand its structure:

```bash
# Quick hex survey of the first 256 bytes
xxd -l 256 shader.pak | head -16

# Check file size
cstat --printf='%s' shader.pak | numfmt --to=iec

# Search for known magic bytes (DXBC, RDEF, ISGN, SHEX, etc.)
rg -c 'DXBC|SHEX|SHDR|RDEF|ISGN|OSGN|STAT' shader.pak
```

**Step 2: Find the Table of Contents (TOC)**

Look for repeating patterns that indicate file entries. Common TOC markers:

| Pattern | Engine/Game | Example |
|---------|-------------|--------|
| `FILELINK_____END` | Warframe/EvoEngine | `_wfshadersdx11.pak` |
| `PK_` (zip-like) | Various | Standard ZIP archives |
| `FSB5` | FMOD | Audio banks |
| `RIFF`/`WAVE` | Generic | RIFF containers |
| Repeating 4-byte offsets | Unreal | `.pak` files |

```bash
# Count occurrences of potential TOC markers
rg -c 'FILELINK' shader.pak

# Look for null-delimited string tables near file start
strings -t x shader.pak | head -50
```

**Step 3: Map the Header**

Most PAK files have a small fixed-size header at offset 0:

```python
import struct

# Read potential header fields
data = open('shader.pak', 'rb').read()

# Try interpreting first 8 bytes as two uint32s
offset_field = struct.unpack_from('<I', data, 0)[0]
count_field = struct.unpack_from('<I', data, 4)[0]

print(f"First u32: 0x{offset_field:08x} ({offset_field})")
print(f"Second u32: {count_field}")

# Validate: does offset_field point to a data region?
# Does count_field match the number of TOC entries?
```

### Warframe/EvoEngine PAK Format (Verified)

This format was fully reverse-engineered from `_wfshadersdx11.pak`:

#### PAK Header (8 bytes)

```
Offset  Size  Field
0x00    4     data_section_offset  (e.g., 0x0000CF70)
0x04    4     entry_count         (e.g., 713)
```

#### TOC Format (entries between header and data section)

Each TOC entry is delimited by the 16-byte marker `FILELINK_____END`:

```
[FILELINK_____END] [padding: NUL bytes]
[4 bytes: file_offset_within_data_section]
[4 bytes: file_size]
[NUL-terminated string: filename] (e.g., "envmesh:terrain_vsh_5.sdrb")
```

#### Per-File Format (SDRB wrapper)

Each `.sdrb` file inside the PAK has a two-layer header before the actual DXBC:

```
[16 bytes: "MANAGEDFILE_DATA"]       <- EvoEngine resource marker
[48 bytes: "BLOCK_USED_IN_ENGINE____________END"]  <- Engine metadata block
[DXBC shader bytecode]               <- Standard Microsoft DirectX bytecode
```

**Key insight**: The DXBC starts at variable offset within each SDRB file. Use `find(b'DXBC')` rather than a fixed offset.

#### DXBC Format (Standard Microsoft)

```
Offset  Size  Field
0x00    4     "DXBC" magic
0x04    16    Content hash (SHA-1 like)
0x14    4     Version (e.g., 0x00050000 for SM5.0)
0x18    4     Total DXBC size in bytes
0x1C    4     Chunk count
0x20    N*4   Chunk offset table (N = chunk count)
[chunk data...]
```

#### DXBC Chunk Types

| Chunk | Description | What It Contains |
|-------|-------------|------------------|
| **RDEF** | Resource Definitions | Constant buffer layouts, texture bindings, sampler bindings, variable names |
| **ISGN** | Input Signature | Vertex inputs (position, normal, UV) or pixel shader inputs from interpolators |
| **OSGN** | Output Signature | Vertex outputs (SV_Position, texcoords) or pixel shader color outputs (SV_TARGET) |
| **SHEX** | Shader Executable | The actual compiled bytecode (DXBC assembly) - SM4/SM5 instructions |
| **SHDR** | Shader Executable (legacy) | Same as SHEX but for older SM2/SM3 shaders |
| **STAT** | Statistics | Instruction count, temp register count, texture load count |

### Extraction Script (Python)

A complete, tested extraction script for this PAK format:

```python
#!/usr/bin/env python3
"""
Generic game shader PAK extractor - Warframe/EvoEngine format.
Usage: python extract_shaders.py <input.pak> <output_dir>
"""
import struct, os, sys
from collections import defaultdict

def read_u32(data, offset):
    return struct.unpack_from('<I', data, offset)[0]

def read_str(data, offset):
    end = offset
    while end < len(data) and data[end] != 0:
        end += 1
    return data[offset:end].decode('ascii', errors='replace')

def parse_pak_toc(pak_data):
    """Parse PAK TOC: header + FILELINK-delimited entries."""
    data_start = read_u32(pak_data, 0)
    entry_count = read_u32(pak_data, 4)
    marker = b'FILELINK_____END'

    # Find all marker positions in TOC region
    positions = []
    pos = 8
    while pos < data_start:
        idx = pak_data.find(marker, pos, data_start)
        if idx == -1:
            break
        positions.append(idx)
        pos = idx + len(marker)

    entries = []
    for i in range(len(positions)):
        entry_start = positions[i] + len(marker)
        entry_end = positions[i + 1] if i + 1 < len(positions) else data_start
        entry_data = pak_data[entry_start:entry_end]

        # Skip leading NULs
        j = 0
        while j < len(entry_data) and entry_data[j] == 0:
            j += 1
        remaining = entry_data[j:]

        if len(remaining) < 8:
            continue

        file_offset = read_u32(remaining, 0)
        file_size = read_u32(remaining, 4)
        nul = remaining.find(b'\x00', 8)
        filename = remaining[8:nul].decode('ascii', errors='replace') if nul > 8 else ""
        entries.append({'name': filename, 'offset': file_offset, 'size': file_size})

    return data_start, entries

def extract_dxbc(pak_data, data_start, entry):
    """Strip SDRB headers to extract raw DXBC."""
    abs_offset = data_start + entry['offset']
    file_data = pak_data[abs_offset:abs_offset + entry['size']]

    # Skip MANAGEDFILE_DATA + BLOCK_USED_IN_ENGINE headers
    dxbc_start = file_data.find(b'DXBC')
    if dxbc_start >= 0:
        return file_data[dxbc_start:]
    return None

def main():
    pak_path = sys.argv[1]
    output_dir = sys.argv[2] or "./extracted_shaders"
    os.makedirs(f"{output_dir}/dxbc_raw", exist_ok=True)
    os.makedirs(f"{output_dir}/disassembled", exist_ok=True)

    data = open(pak_path, 'rb').read()
    data_start, entries = parse_pak_toc(data)

    extracted = 0
    for entry in entries:
        dxbc = extract_dxbc(data, data_start, entry)
        if dxbc and len(dxbc) > 64:
            clean = entry['name'].replace(':', '_').replace('/', '_')
            open(f"{output_dir}/dxbc_raw/{clean}.dxbc", 'wb').write(dxbc)
            extracted += 1

    print(f"Extracted {extracted} shaders from {len(entries)} entries")

if __name__ == '__main__':
    main()
```

### DXBC Disassembly

For quick inspection of extracted DXBC files, use Microsoft's DXC:

```bash
# Disassemble to DXBC ASM (text format)
dxc -dumpbin shader.dxbc -Fc output.asm

# Or use the standalone DXBC disassembler from Windows SDK
dxbcdisasm shader.dxbc
```

For programmatic disassembly (Python), the full DXBC bytecode decoder from the Warframe extraction covers:

- **Opcode decoding**: 180+ SM4/SM5 instructions (add, mad, mul, sample, dp4, etc.)
- **Operand parsing**: Register types (temp, input, output, imm), swizzle masks, write masks
- **Signature parsing**: ISGN/OSGN semantic names (POSITION, TEXCOORD, SV_TARGET)
- **Resource definitions**: Constant buffer bindings (cbuffer/register(b#)), texture bindings (Texture2D/register(t#))
- **Statistics extraction**: Instruction count, temp register count, texture loads

#### DXBC Opcode Quick Reference

The most common opcodes found in game shaders:

| Opcode | Name | Category |
|--------|------|----------|
| 0x31 | `mad` | Arithmetic (multiply-add) |
| 0x34 | `mul` | Arithmetic |
| 0x00 | `add` | Arithmetic |
| 0x42 | `sample` | Texture sampling |
| 0x45 | `sample_l` | Texture with LOD |
| 0x43 | `sample_c` | Texture with comparison |
| 0x10 | `dp4` | Dot product (4-component) |
| 0x0E | `dp2` | Dot product (2-component) |
| 0x0F | `dp3` | Dot product (3-component) |
| 0x4B | `sqrt` | Math |
| 0x41 | `rsq` | Math (reciprocal sqrt) |
| 0x18 | `exp` | Math |
| 0x2E | `log` | Math |
| 0x4A | `sin` | Trig |
| 0x1B | `ftou` | Conversion (float to uint) |
| 0x2A | `itof` | Conversion (int to float) |
| 0x33 | `max` / 0x32 | `min` | Comparison |
| 0x19 | `frc` | Fractional |
| 0x0C | `discard` | Flow control |
| 0x3A | `ret` | Flow control |
| 0x2F | `loop` / 0x15 | `endloop` | Flow control |
| 0x5A | `dcl_constantbuffer` | Declaration |
| 0x59 | `dcl_resource` | Declaration |
| 0x5B | `dcl_sampler` | Declaration |

#### Register Types in DXBC

| Register | Name | Usage |
|----------|------|-------|
| `r#` | Temp register | Temporary computation results |
| `v#` | Input register | Vertex inputs / interpolators |
| `o#` | Output register | Vertex outputs / color outputs |
| `immcb#` | Imm constant buffer | Inline constants (cb0-cb15) |
| `icb` | Immediate constant buffer | Literal values embedded in shader |
| `x#` | Indexable temp | Array-indexable temporaries |
| `null` | Null register | Discarded results |
| `id#` | Instance ID | Geometry shader instance |
| `s#` | Sampler | Sampler state binding |
| `t#` | Texture | Shader resource view |

### Tips for Unknown PAK Formats

When facing an unknown PAK format, follow this systematic approach:

1. **Hex dump the first 1KB** to look for patterns, magic strings, and structure
2. **Search for `DXBC`** to locate shader bytecode and work backwards to find the TOC entries that reference those offsets
3. **Look for filename strings** near the DXBC locations (filenames are usually adjacent to offset/size metadata)
4. **Count patterns** to verify your header interpretation (entry count should match the number of delimiter repetitions)
5. **Validate by extraction**: Extract a candidate file and verify the first 4 bytes are `DXBC` (0x44, 0x58, 0x42, 0x43)
6. **Handle empty entries**: Some games use placeholder files (size < 64 bytes or all zeros) - skip them
7. **Look for wrapper headers**: Many engines wrap DXBC with custom headers (MANAGEDFILE_DATA, BLOCK_USED_IN_ENGINE, etc.) - use `find(b'DXBC')` to locate the real start

### Real-World Results (Warframe Extraction)

| Metric | Value |
|--------|-------|
| Total PAK entries | 713 |
| Successfully extracted | 678 shaders |
| Empty/placeholder | 35 entries |
| Vertex shaders (vsh) | 226 |
| Pixel shaders (psh) | 452 |
| Total bytecode | 2.7 MB |
| Total instructions | 54,944 |
| Largest shader | `uberpost.psh_63` (398 instructions, 14120 bytes) |
| Shader categories | 28 (anim2d, artparticle, envmesh, uberpost, etc.) |
| Largest category | envmesh (348 shaders, 1375 KB) |

---

## Workflows

### Creating Shaders

1. Identify target platform → determine language
2. Select shader type: **vertex** (geometry transform), **fragment** (pixel color), **compute** (parallel compute)
3. Use appropriate template from below
4. Define inputs (attributes, uniforms, varyings)
5. Implement main function with correct semantics

### Analyzing Shaders

Detect shader type from content:
- `SV_Position` output / `gl_Position` assignment → **Vertex**
- `SV_TARGET` output / `gl_FragColor` / `out vec4` → **Fragment**
- `numthreads` / `local_size_x` / `@compute` → **Compute**

### Converting Shaders

1. Identify source language and shader type
2. Apply type conversions (see Type Mapping tables)
3. Convert function calls (see Intrinsic Functions tables)
4. Translate semantics (see Semantic Mapping tables)
5. Adjust entry point syntax
6. Add language-specific headers/directives
7. Handle platform differences (coordinate systems, matrix layout)

### Performance Analysis Workflow

1. Write initial shader code
2. Run through target API (OpenGL/Vulkan)
3. Extract compiled shader from NVIDIA cache
4. Disassemble with nvdisasm
5. Analyze instruction counts
6. Identify STL/LDL hotspots
7. Optimize source code
8. Re-extract and compare

---

## Practical Patterns (Copy-Paste Ready)

### Noise Functions

#### Value Noise (2D)
```glsl
float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

float valueNoise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    f = f * f * (3.0 - 2.0 * f); // Smoothstep
    
    float a = hash(i);
    float b = hash(i + vec2(1.0, 0.0));
    float c = hash(i + vec2(0.0, 1.0));
    float d = hash(i + vec2(1.0, 1.0));
    
    return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
}
```

#### Perlin Noise (2D)
```glsl
vec2 hash22(vec2 p) {
    p = vec2(dot(p, vec2(127.1, 311.7)), dot(p, vec2(269.5, 183.3)));
    return -1.0 + 2.0 * fract(sin(p) * 43758.5453);
}

float perlinNoise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);
    
    float a = dot(hash22(i), f - vec2(0.0, 0.0));
    float b = dot(hash22(i + vec2(1.0, 0.0)), f - vec2(1.0, 0.0));
    float c = dot(hash22(i + vec2(0.0, 1.0)), f - vec2(0.0, 1.0));
    float d = dot(hash22(i + vec2(1.0, 1.0)), f - vec2(1.0, 1.0));
    
    return mix(mix(a, b, f.x), mix(c, d, f.x), f.y) * 0.5 + 0.5;
}
```

#### Fractal Brownian Motion (FBM)
```glsl
float fbm(vec2 p, int octaves) {
    float value = 0.0;
    float amplitude = 0.5;
    float frequency = 1.0;
    
    for (int i = 0; i < octaves; i++) {
        value += amplitude * perlinNoise(p * frequency);
        amplitude *= 0.5;
        frequency *= 2.0;
    }
    return value;
}
```

#### Voronoi/Cellular Noise
```glsl
vec2 voronoi(vec2 p) {
    vec2 n = floor(p);
    vec2 f = fract(p);
    
    float minDist = 1.0;
    float secondMin = 1.0;
    
    for (int j = -1; j <= 1; j++) {
        for (int i = -1; i <= 1; i++) {
            vec2 neighbor = vec2(float(i), float(j));
            vec2 point = neighbor + hash(n + neighbor) - f;
            float dist = length(point);
            
            if (dist < minDist) {
                secondMin = minDist;
                minDist = dist;
            } else if (dist < secondMin) {
                secondMin = dist;
            }
        }
    }
    return vec2(minDist, secondMin); // (distance, edge)
}
```

---

### Lighting Models

#### Lambert (Diffuse Only)
```glsl
float lambert(vec3 normal, vec3 lightDir) {
    return max(dot(normal, lightDir), 0.0);
}
```

#### Blinn-Phong
```glsl
vec3 blinnPhong(vec3 normal, vec3 lightDir, vec3 viewDir, 
                vec3 albedo, vec3 specColor, float shininess) {
    vec3 halfDir = normalize(lightDir + viewDir);
    float NdotL = max(dot(normal, lightDir), 0.0);
    float NdotH = max(dot(normal, halfDir), 0.0);
    float specular = pow(NdotH, shininess);
    return albedo * NdotL + specColor * specular;
}
```

#### Fresnel (Schlick Approximation)
```glsl
vec3 fresnelSchlick(float cosTheta, vec3 F0) {
    return F0 + (1.0 - F0) * pow(1.0 - cosTheta, 5.0);
}

vec3 fresnelSchlickRoughness(float cosTheta, vec3 F0, float roughness) {
    return F0 + (max(vec3(1.0 - roughness), F0) - F0) * pow(1.0 - cosTheta, 5.0);
}
```

#### GGX/Trowbridge-Reitz (Normal Distribution)
```glsl
const float PI = 3.14159265359;

float distributionGGX(vec3 N, vec3 H, float roughness) {
    float a = roughness * roughness;
    float a2 = a * a;
    float NdotH = max(dot(N, H), 0.0);
    float NdotH2 = NdotH * NdotH;
    float denom = (NdotH2 * (a2 - 1.0) + 1.0);
    denom = PI * denom * denom;
    return a2 / denom;
}
```

#### Full PBR (Cook-Torrance BRDF)
```glsl
float geometrySchlickGGX(float NdotV, float roughness) {
    float r = (roughness + 1.0);
    float k = (r * r) / 8.0;
    return NdotV / (NdotV * (1.0 - k) + k);
}

float geometrySmith(vec3 N, vec3 V, vec3 L, float roughness) {
    float NdotV = max(dot(N, V), 0.0);
    float NdotL = max(dot(N, L), 0.0);
    return geometrySchlickGGX(NdotV, roughness) * geometrySchlickGGX(NdotL, roughness);
}

vec3 pbrBRDF(vec3 N, vec3 V, vec3 L, vec3 albedo, float metallic, float roughness, vec3 lightColor) {
    vec3 H = normalize(V + L);
    vec3 F0 = mix(vec3(0.04), albedo, metallic);
    
    float NDF = distributionGGX(N, H, roughness);
    float G = geometrySmith(N, V, L, roughness);
    vec3 F = fresnelSchlick(max(dot(H, V), 0.0), F0);
    
    vec3 specular = (NDF * G * F) / (4.0 * max(dot(N, V), 0.0) * max(dot(N, L), 0.0) + 0.0001);
    vec3 kD = (1.0 - F) * (1.0 - metallic);
    
    return (kD * albedo / PI + specular) * lightColor * max(dot(N, L), 0.0);
}
```

---

## GPU Performance Optimization

### Cardinal Rule

**Every optimization must produce visually identical output.** If you can't prove the math is equivalent, don't suggest the change. "Close enough" is not acceptable for aesthetic shaders.

---

### Optimization Validation Methodology

**CRITICAL**: Before suggesting any function replacement or algebraic simplification, you MUST verify mathematical equivalence through testing. A replacement is only valid if the resulting equation produces **equal values** (for exact replacements) or **very close approximation** (for approximations) across the expected input range.

#### Validation Requirements

For every function replacement suggestion, you must:

1. **Identify all variables** in both the original and replacement expressions
2. **Test with at least 3 different values** for each variable
3. **Verify results match** within acceptable tolerance
4. **Document any edge cases** or domain restrictions

#### Tolerance Thresholds

| Replacement Type | Maximum Acceptable Error | Notes |
|------------------|-------------------------|-------|
| **Exact mathematical equivalence** | 0 (bit-identical) | Must be provably identical |
| **Very close approximation** | < 0.001 relative error | For visual output, imperceptible difference |
| **Approximation** | < 0.01 relative error | Requires explicit user consent |

#### Test Value Selection

When testing replacements, select test values that cover:

- **Typical values**: Common use case inputs (e.g., 0.5 for normalized values)
- **Boundary values**: Edge of valid domain (e.g., 0.0, 1.0 for colors)
- **Edge cases**: Potential problem areas (e.g., negative values, very small/large values)

**Minimum test values per variable: 3**

```hlsl
// Example: Testing pow(x, 2.0) → x * x
// Variables: x
// Test values: x = 0.5, x = 2.0, x = -1.5

// Test 1: x = 0.5
pow(0.5, 2.0) = 0.25
0.5 * 0.5     = 0.25  ✓ MATCH

// Test 2: x = 2.0
pow(2.0, 2.0) = 4.0
2.0 * 2.0     = 4.0  ✓ MATCH

// Test 3: x = -1.5
pow(-1.5, 2.0) = 2.25
-1.5 * -1.5    = 2.25  ✓ MATCH

// VERDICT: Safe replacement (exact equivalence proven)
```

#### Validated Replacement Categories

**Category A: Exact Equivalence (No validation needed for standard cases)**

These replacements are mathematically identical and can be applied without per-case testing:

| Original | Replacement | Proof |
|----------|-------------|-------|
| `pow(x, 2.0)` | `x * x` | x² = x × x by definition |
| `pow(x, 3.0)` | `x * x * x` | x³ = x × x × x by definition |
| `pow(x, 4.0)` | `x2 = x*x; x2*x2` | x⁴ = (x²)² by definition |
| `pow(x, 0.5)` | `sqrt(x)` | x^0.5 = √x by definition (x ≥ 0) |
| `length(v) * length(v)` | `dot(v, v)` | |v|² = v·v by definition |
| `abs(x) * abs(x)` | `x * x` | |x|² = x² by definition |
| `1.0 - (1.0 - x)` | `x` | 1 - (1 - x) = x algebraic identity |
| `x * 1.0` | `x` | Multiplicative identity |
| `x + 0.0` | `x` | Additive identity |

**Category B: Close Approximation (Requires testing for each use case)**

These replacements approximate the original function and require validation:

| Original | Approximation | Test Required | Error Characteristic |
|----------|---------------|---------------|---------------------|
| `pow(x, 2.2)` | `x * x * pow(x, 0.2)` | Yes | Varies with x |
| `exp(x)` (|x| < 0.5) | `1 + x + 0.5*x*x` | Yes | Taylor series truncation |
| `sin(x)` (small x) | `x - x³/6` | Yes | Taylor series truncation |
| `atan(x)` (|x| < 1) | `x / (1 + 0.28*x²)` | Yes | Padé approximation |

**Category C: Context-Dependent (Requires domain analysis)**

These replacements depend on input domain and context:

| Original | Replacement | Validation Required |
|----------|-------------|---------------------|
| `clamp(x, 0.0, 1.0)` | `saturate(x)` | Verify x is float, GPU supports saturate |
| `normalize(v)` | Skip when |v| = 1 | Verify v is already unit length |
| `x / y` | `x * (1.0 / y)` | Verify y is constant or hoisted |
| `log(x) / log(2.0)` | `log2(x)` | Verify x > 0 |

#### Validation Procedure Template

```hlsl
// VALIDATION REPORT: [Original] → [Replacement]
// ===============================================

// Variables: [list all variables]

// Test Case 1: [variable values]
original_result = [computed value]
replacement_result = [computed value]
error = abs(original_result - replacement_result)
status = [PASS/FAIL]

// Test Case 2: [variable values]
original_result = [computed value]
replacement_result = [computed value]
error = abs(original_result - replacement_result)
status = [PASS/FAIL]

// Test Case 3: [variable values]
original_result = [computed value]
replacement_result = [computed value]
error = abs(original_result - replacement_result)
status = [PASS/FAIL]

// VERDICT: [APPROVED/REJECTED/NEEDS_MORE_TESTING]
// Notes: [any edge cases or warnings]
```

#### Example: Validating exp(x) Taylor Approximation

```hlsl
// VALIDATION REPORT: exp(x) → 1 + x + 0.5*x*x (for small x)
// ==========================================================

// Claim: For |x| < 0.5, Taylor series approximation is valid

// Test Case 1: x = 0.1
exp(0.1)           = 1.105170918...
1 + 0.1 + 0.05     = 1.150000000...
error              = 0.0448 (4.48% relative error)
status             = FAIL - Error too high

// Test Case 2: x = 0.2
exp(0.2)           = 1.221402758...
1 + 0.2 + 0.02     = 1.220000000...
error              = 0.0014 (0.11% relative error)
status             = MARGINAL

// Test Case 3: x = 0.3
exp(0.3)           = 1.349858808...
1 + 0.3 + 0.045    = 1.345000000...
error              = 0.00486 (0.36% relative error)
status             = MARGINAL

// VERDICT: REJECTED for precision-critical code
// The 2nd-order Taylor series has significant error even for small x.
// Recommend using 3rd-order: 1 + x + 0.5*x² + x³/6 for |x| < 0.5
```

#### Example: Validating sin(x) Small Angle Approximation

```hlsl
// VALIDATION REPORT: sin(x) → x - x³/6 (for small x in radians)
// ==============================================================

// Test Case 1: x = 0.1 radians
sin(0.1)           = 0.099833417...
0.1 - 0.001/6      = 0.099833333...
error              = 0.000000084 (0.00008% relative error)
status             = PASS - Excellent approximation

// Test Case 2: x = 0.3 radians
sin(0.3)           = 0.295520207...
0.3 - 0.027/6      = 0.295500000...
error              = 0.000020207 (0.0068% relative error)
status             = PASS - Very good approximation

// Test Case 3: x = 0.5 radians
sin(0.5)           = 0.479425539...
0.5 - 0.125/6      = 0.479166667...
error              = 0.000258872 (0.054% relative error)
status             = PASS - Good approximation for visual use

// VERDICT: APPROVED for |x| < 0.5 radians with visual tolerance
// Error remains below 0.1% for angles up to ~28 degrees
// WARNING: Do not use for angles > 0.5 radians without additional terms
```

---

### Performance Context

At high frame rates (120-240fps) on high-resolution displays (1440p+), every pixel shader instruction runs hundreds of millions of times per second. Even saving one ALU instruction matters. At 240fps on 1440p with half the overlay visible: ~885M pixel shader executions per second (3840×1600×240÷2).

### 1. Transcendental Optimizations (Highest Priority)

Transcendental functions (`sin`, `cos`, `atan2`, `exp`, `log`, `pow`) are the most expensive GPU instructions.

#### Sin/Cos Optimization

**Paired sin/cos of the same angle** → Use `sincos`:
```hlsl
// BEFORE — 2 transcendentals
float s = sin(angle);
float c = cos(angle);

// AFTER — 1 intrinsic (HLSL/MSL)
float s, c;
sincos(angle, s, c);

// GLSL equivalent
float s = sin(angle);
float c = cos(angle);
// No sincos in GLSL, but still hoist repeated calls
```

**Repeated sin/cos calls with the same argument** → Hoist to local variable:
```hlsl
// BEFORE — sin(time * 0.1) computed 3 times
x += sin(time * 0.1) * 2.0;
y += sin(time * 0.1) * 3.0;
z += sin(time * 0.1);

// AFTER — computed once
float st = sin(time * 0.1);
x += st * 2.0;
y += st * 3.0;
z += st;
```

#### Power Function Optimization

**IMPORTANT**: Power function replacements fall into two categories:

| Pattern | Replacement | Validation Status | Requirements |
|---------|-------------|-------------------|--------------|
| `pow(x, 2.0)` | `x * x` | ✅ **VALIDATED** | Exact equivalence - always safe |
| `pow(x, 0.5)` | `sqrt(x)` | ✅ **VALIDATED** | Exact equivalence for x ≥ 0 |
| `pow(x, 3.0)` | `x * x * x` | ✅ **VALIDATED** | Exact equivalence - always safe |
| `pow(x, 4.0)` | `x2 = x * x; x2 * x2` | ✅ **VALIDATED** | Exact equivalence - always safe |
| `pow(x, 2.2)` | Various approximations | ⚠️ **NEEDS TESTING** | Test 3+ values before use |

```hlsl
// VALIDATED REPLACEMENT: pow(x, 2.0) → x * x
// Proof: By definition, x² = x × x
// Test values: x = 0.5, 2.0, -1.5 → All match exactly

// BEFORE — transcendental
float brightness = pow(color, 2.0);

// AFTER — ALU only (SAFE)
float brightness = color * color;
```

```hlsl
// APPROXIMATION REQUIRES TESTING: pow(color, 2.2) approximations
// The following are approximations, not exact replacements:

// For gamma correction, pow(x, 1.0/2.2):
// BEFORE
float gamma = pow(color, 1.0/2.2);

// AFTER — faster but approximate
float gamma = sqrt(color); // gamma 2.0 (different from 2.2!)

// VALIDATION for gamma 2.0 vs 2.2:
// Test Case 1: color = 0.5
// pow(0.5, 1/2.2) = 0.730
// sqrt(0.5)       = 0.707  (3.2% error)
// VERDICT: Significant difference — may be visually noticeable

// If closer approximation needed:
float gamma = sqrt(sqrt(color * color * color)); // gamma ~2.17
// Test: pow(0.5, 1/2.2) = 0.730, approx = 0.741 (1.5% error)
// BETTER but still approximate — test in context!
```

#### Other Transcendental Patterns

```hlsl
// VALIDATED: log(x) / log(2.0) → log2(x)
// Proof: log₂(x) = ln(x)/ln(2) by change of base formula
// BEFORE
float result = log(x) / log(2.0);

// AFTER (SAFE for x > 0)
float result = log2(x);  // Single instruction
```

```hlsl
// APPROXIMATION: exp(x) Taylor series
// BEFORE
float result = exp(x);

// AFTER (for |x| < 1, requires testing)
float result = 1.0 + x + 0.5 * x * x;

// VALIDATION REQUIRED:
// Test x = 0.5: exp(0.5) = 1.649, approx = 1.625 (1.5% error)
// Test x = 0.3: exp(0.3) = 1.350, approx = 1.345 (0.4% error)
// Test x = 1.0: exp(1.0) = 2.718, approx = 2.500 (8.0% error) — UNACCEPTABLE
// VERDICT: Only valid for |x| < 0.5 with visual tolerance
```

### 2. Normalization Optimizations

```hlsl
// VALIDATED: normalize() skip when length is known
// Context: float3(cos(a), sin(a), 0.0) has unit length by trigonometric identity
float3 dir = float3(cos(a), sin(a), 0.0);  // Already unit length
// Don't: dir = normalize(dir);  // Wasteful - proven unnecessary

// VALIDATED: Repeated normalize of same vector → Hoist
// BEFORE
float3 n1 = normalize(v);
float3 n2 = normalize(v);  // Redundant

// AFTER
float3 n = normalize(v);

// VALIDATED: length(v) * length(v) → dot(v, v)
// Proof: |v|² = v·v by definition
// BEFORE
float lenSq = length(v) * length(v);  // 2 length calls (sqrt operations)

// AFTER (SAFE)
float lenSq = dot(v, v);  // No sqrt, exact equivalence

// If both length and normalized vector needed:
// BEFORE
float len = length(v);
float3 n = v / len;

// AFTER (if len actually needed)
float lenSq = dot(v, v);
float len = sqrt(lenSq);
float3 n = v * rsqrt(lenSq);  // rsqrt is single instruction
```

### 3. Loop Optimizations

#### Loop-Invariant Code Motion

```hlsl
// BEFORE — rotation computed every iteration
for (int i = 0; i < 8; i++) {
    float2x2 rot = float2x2(cos(angle), sin(angle), -sin(angle), cos(angle));
    p = mul(p, rot);
    total += noise(p);
}

// AFTER — rotation computed once
float s, c;
sincos(angle, s, c);
float2x2 rot = float2x2(c, s, -s, c);
for (int i = 0; i < 8; i++) {
    p = mul(p, rot);
    total += noise(p);
}
```

#### Accumulator Patterns

```hlsl
// Common FBM pattern
float total = 0.0;
float amp = 0.5;
float2 p = uv;
for (int i = 0; i < 6; i++) {
    total += noise(p) * amp;
    p = mul(p, float2x2(1.6, 1.2, -1.2, 1.6));  // Rotate and scale
    amp *= 0.5;
}
```

### 4. Matrix and Vector Math

#### Rotation Matrix Optimization

```hlsl
// BEFORE — per-pixel (wasteful if angle is uniform from cbuffer)
float2x2 rot = float2x2(cos(a), sin(a), -sin(a), cos(a));

// AFTER — single sincos + construction
float s, c;
sincos(a, s, c);
float2x2 rot = float2x2(c, s, -s, c);
```

**Note**: HLSL `static` local variables are computed once per draw call, not per-pixel:
```hlsl
// This is computed per-pixel
float2x2 getRotation(float angle) {
    return float2x2(cos(angle), sin(angle), -sin(angle), cos(angle));
}

// This is computed once (if angle is compile-time constant)
static const float2x2 rot90 = float2x2(0, 1, -1, 0);
```

#### Matrix Multiplication Order

```hlsl
// HLSL matrix multiplication convention:
// Vector-matrix: mul(v, M) — v treated as row vector
// Matrix-vector: mul(M, v) — v treated as column vector

// For column-major storage (GLSL default):
float4 result = mul(M, v);  // M * v

// For row-major storage (HLSL default):
float4 result = mul(v, M);  // v * M
```

### 5. Texture Sampling Efficiency

```hlsl
// Redundant samples → Hoist
// BEFORE
float4 a = tex2D(sampler, uv);
float4 b = tex2D(sampler, uv);  // Same UV!
float4 c = tex2D(sampler, uv);  // Same UV!

// AFTER
float4 tex = tex2D(sampler, uv);
float4 a = tex;
float4 b = tex;
float4 c = tex;

// Sample in divergent branch → Note but don't auto-change
// Can cause quad inefficiency on some GPUs
if (condition) {
    float4 tex = tex2D(sampler, uv);  // Potential issue
}
```

### 6. Algebraic Simplifications (With Validation Status)

| Pattern | Simplification | Validation | Savings |
|---------|----------------|------------|---------|
| `x * 0.5 + 0.5` | `mad(x, 0.5, 0.5)` or leave as-is | ✅ Exact | Compiler usually handles |
| `1.0 - (1.0 - x)` | `x` | ✅ Exact | 2 operations → 0 |
| `a / b * c` (b constant) | `a * (c / b)` | ✅ Exact | 1 divide + 1 multiply → 1 multiply |
| `length(v) * length(v)` | `dot(v, v)` | ✅ Exact | Avoids sqrt |
| `abs(x) * abs(x)` | `x * x` | ✅ Exact | 1 abs + 1 mul → 1 mul |
| `clamp(x, 0.0, 1.0)` | `saturate(x)` | ✅ Exact | Free on most GPUs (modifier) |
| `smoothstep(0.0, 1.0, x)` | `x*x*(3.0 - 2.0*x)` | ✅ Exact | Same cost, explicit |
| `frac(x / 1.0)` | `frac(x)` | ✅ Exact | No-op removal |
| `floor(x / 1.0)` | `floor(x)` | ✅ Exact | No-op removal |
| `x / 2.0` | `x * 0.5` | ✅ Exact | Often faster (no divide) |
| `pow(x, 2.0)` | `x * x` | ✅ Exact | Transcendental → ALU |
| `pow(x, 3.0)` | `x * x * x` | ✅ Exact | Transcendental → ALU |
| `pow(x, 0.5)` | `sqrt(x)` | ✅ Exact (x≥0) | Dedicated hardware |
| `pow(x, 2.2)` | Approximation | ⚠️ **TEST REQUIRED** | Not exact - see notes below |
| `exp(x)` (small x) | `1+x+0.5x²` | ⚠️ **TEST REQUIRED** | Taylor approximation |

```hlsl
// EXAMPLE: Validating smoothstep equivalence
// Test Case 1: x = 0.25
smoothstep(0.0, 1.0, 0.25) = 0.15625
0.25*0.25*(3.0-2.0*0.25)   = 0.15625  ✓

// Test Case 2: x = 0.5
smoothstep(0.0, 1.0, 0.5)  = 0.5
0.5*0.5*(3.0-2.0*0.5)      = 0.5  ✓

// Test Case 3: x = 0.75
smoothstep(0.0, 1.0, 0.75) = 0.84375
0.75*0.75*(3.0-2.0*0.75)   = 0.84375  ✓

// VERDICT: Exact equivalence confirmed
```

### 7. Conversion Artifacts (GLSL → HLSL)

| Issue | GLSL Original | Bad HLSL | Correct HLSL | Validation |
|-------|---------------|----------|--------------|------------|
| Modulo | `mod(x, 1.0)` | `fmod(x, 1.0)` | `frac(x)` | ⚠️ Only for positive x |
| Modulo (general) | `mod(x, y)` | `fmod(x, y)` | `x - y * floor(x/y)` | ✅ Exact |
| Texture | `texture(tex, uv)` | Various | `tex.Sample(samp, uv)` | ✅ Direct mapping |
| FragCoord | `gl_FragCoord.xy` | Various | `pos.xy` (from SV_Position) | ✅ Direct mapping |

```hlsl
// VALIDATION: fmod vs frac for mod(x, 1.0)
// Test Case 1: x = 2.5
mod(2.5, 1.0) = 0.5
frac(2.5)     = 0.5  ✓

// Test Case 2: x = -0.5
mod(-0.5, 1.0) = 0.5 (GLSL behavior)
frac(-0.5)     = -0.5 (different!)  ✗

// VERDICT: frac(x) is ONLY equivalent to mod(x, 1.0) for x >= 0
// For negative x, use: x - floor(x) instead
```

```hlsl
// fmod vs frac
// BEFORE (from mechanical conversion)
float wrap = fmod(x, 1.0);  // Expensive: involves division

// AFTER (SAFE for x >= 0)
float wrap = frac(x);  // Single instruction

// AFTER (SAFE for all x, matches GLSL mod behavior)
float wrap = x - floor(x);

// Dead code from removed features
// iMouse handling often zeroed but code still computes:
float2 mouse = float2(0.0, 0.0);  // Dead
float2 dir = normalize(mouse - uv);  // Computes garbage
// Simplify away entire dead code paths
```

### 8. Constant Folding Hints

```hlsl
// static const for compile-time evaluation
static const float PI = 3.14159265;
static const float TWO_PI = 2.0 * PI;  // Computed at compile time
static const float INV_PI = 1.0 / PI;

// Literal precision
// BEFORE
float x = 3.14159265358979323846;  // Wastes parser time

// AFTER
float x = 3.14159265f;  // Only 7 significant digits in float

// Integer vs float constants
// Use 2.0 instead of 2 in float contexts to avoid implicit cast
float half_val = x / 2.0;  // Clear intent
```

### 9. Compute Shader Optimizations

```hlsl
[numthreads(64, 1, 1)]
void CSMain(uint3 id : SV_DispatchThreadID)
{
    uint idx = id.x;
    if (idx >= totalElements) return;  // Guard for non-multiple-of-64

    // Early-exit checks FIRST (before expensive operations)
    if (p.life >= 1.0) return;  // Skip dead particles first

    // Radius check BEFORE computing glow/color
    if (dist > maxRadius) return;  // Skip far particles

    // Avoid redundant normalize
    // BEFORE
    float3 dir = normalize(target - pos);
    float3 dir2 = normalize(target - pos);  // Redundant!

    // AFTER
    float3 dir = normalize(target - pos);
    // Reuse 'dir'
}
```

#### Compute Shader Key Patterns

1. **Early-exit ordering**: Skip dead particles (`life >= 1.0`) as first check
2. **Radius check before glow**: Check distance before computing expensive color
3. **Avoid redundant normalize**: Cache normalized vectors
4. **Dispatch thread count**: Guard `if (idx >= total) return;` is necessary for non-multiple-of-64 buffer sizes
5. **Config-driven sizing**: Grid dimensions and counts may be runtime values from cbuffer

### 10. Optimization Validation Checklist

- [ ] Prove mathematical equivalence for all changes OR document approximation error
- [ ] Test with at least 3 different values for each variable
- [ ] Check original source if converted - some "inefficiencies" may be intentional
- [ ] Verify visual output is identical (for exact replacements)
- [ ] Respect author intent (artistic choices in pow curves, etc.)
- [ ] Mark uncertain cases as "needs visual verification"
- [ ] Document any domain restrictions (e.g., "valid for x >= 0 only")

### Optimization Assessment Format

| Pattern | Affected Locations | Per-Pixel Cost Saved | Validation Status | Fix |
|---------|-------------------|---------------------|-------------------|-----|
| Paired sin/cos → sincos | `fire.hlsl:45`, +12 more | ~1 transcendental | ✅ Exact | `sincos(angle, s, c)` |
| `pow(x, 2.0)` → `x * x` | `glow.hlsl:78`, +3 more | ~1 transcendental | ✅ Exact | `x * x` |
| `pow(color, 2.2)` → approximation | `gamma.hlsl:23` | ~1 transcendental | ⚠️ Test needed | Verify visually |

---

## Platform Gotchas

### Coordinate System Differences

| Platform | Origin | Y Direction | Depth Range |
|----------|--------|-------------|-------------|
| DirectX | Top-left | Y down | [0, 1] |
| OpenGL | Bottom-left | Y up | [-1, 1] |
| Vulkan | Top-left | Y down | [0, 1] |
| Metal | Top-left | Y down | [0, 1] |
| WebGL | Bottom-left | Y up | [-1, 1] |

```glsl
// OpenGL to DirectX UV flip
vec2 dxUV = vec2(uv.x, 1.0 - uv.y);

// DirectX to OpenGL depth mapping
float glDepth = depth * 2.0 - 1.0;
```

### Matrix Layout

```hlsl
// HLSL default: row-major
float4x4 mat;  // mat[0] is the first ROW

// GLSL default: column-major
mat4 mat;  // mat[0] is the first COLUMN

// Matrix multiplication order
// HLSL: mul(vector, matrix) - vector on left
// GLSL: matrix * vector - vector on right
```

### Mod Function Differences

```hlsl
// GLSL mod() vs HLSL fmod() behave differently for negative numbers
// GLSL: mod(-3.0, 2.0) = 1.0
// HLSL: fmod(-3.0, 2.0) = -1.0

// Portable mod for HLSL
float mod(float x, float y) {
    return x - y * floor(x / y);
}
```

### ReShade FX Specific Gotchas

**CRITICAL**: ReShade FX does NOT include `fmod` among its intrinsic functions, unlike standard HLSL. This is a common mistake when porting HLSL shaders to ReShade.

```hlsl
// WRONG - fmod does not exist in ReShade FX
float wrapped = fmod(x, 1.0);  // Compile error!

// CORRECT - Use custom helper function
float wrapped = x - floor(x);  // Equivalent to frac(x) for positive x

// CORRECT - Full GLSL-style mod implementation for ReShade
float mod(float x, float y) {
    return x - y * floor(x / y);
}

// For wrapping values (most common use case):
// Instead of: fmod(time, 1.0)
float wrapped = frac(time);  // Works for positive values

// Instead of: fmod(coord, 2.0) - for wrapping coordinates
float2 wrappedCoord = frac(coord / 2.0) * 2.0;  // Wraps to [0, 2)
```

**ReShade FX Missing Intrinsics Reference:**

| Function | Standard HLSL | ReShade FX | Workaround |
|----------|---------------|------------|------------|
| Modulo | `fmod(x, y)` | ❌ Not available | `x - y * floor(x / y)` |
| Fractional wrap | `fmod(x, 1.0)` | ❌ Not available | `frac(x)` (positive x only) |
| Remainder | `%` operator | ❌ Not available | Custom function |

**Safe ReShade Mod Helper Functions:**

```hlsl
// Add these to your ReShade shaders when you need modulo operations

// GLSL-compatible mod (handles negative numbers correctly)
float mod(float x, float y) {
    return x - y * floor(x / y);
}
float2 mod(float2 x, float2 y) {
    return x - y * floor(x / y);
}
float3 mod(float3 x, float3 y) {
    return x - y * floor(x / y);
}
float4 mod(float4 x, float4 y) {
    return x - y * floor(x / y);
}

// For simple 0-1 wrapping (positive values only, faster)
// frac(x) is available in ReShade and equals x - floor(x)
```

### Precision Differences

```glsl
// WebGL 1.0 requires precision qualifiers
precision mediump float;  // ~16-bit
precision highp float;    // ~32-bit

// Mobile GPU precision pitfalls
// - mediump may introduce banding
// - lowp sufficient for colors (0-1 range)
// - highp needed for positions, depths
```

---

## Troubleshooting Guide

### Common Errors & Solutions

| Error Message | Cause | Solution |
|--------------|-------|----------|
| `Cannot resolve symbol` | Undefined variable/function | Check spelling, includes |
| `Type mismatch` | Wrong type in expression | Match vec/mat sizes |
| `Uninitialized variable` | Variable used before set | Initialize all variables |
| `Division by zero` | Constant 0 divisor | Guard with condition |

### Black Screen Debug

```hlsl
return float4(1, 0, 0, 1);  // If red, shader runs
return float4(normal * 0.5 + 0.5, 1);  // Visualize normals
return float4(uv, 0, 1);  // Visualize UVs
return float4(depth.rrr, 1);  // Visualize depth
```

### NaN/Inf Detection

```hlsl
bool isNaN(float x) { return x != x; }
bool isInf(float x) { return x == x * 2.0 && x != 0.0; }

float safeDiv(float a, float b) { return a / (b + 1e-6); }
float safeSqrt(float x) { return sqrt(max(0.0, x)); }
float safeAcos(float x) { return acos(clamp(x, -1.0, 1.0)); }
```

---

## Type Mapping

### Scalar Types

| HLSL | GLSL | MSL | WGSL |
|------|------|-----|------|
| `float` | `float` | `float` | `f32` |
| `int` | `int` | `int` | `i32` |
| `uint` | `uint` | `uint` | `u32` |
| `bool` | `bool` | `bool` | `bool` |
| `half` | `float` (ES: `mediump`) | `half` | `f16` |
| `double` | `double` | `double` | `f64` |

### Vector Types

| HLSL | GLSL | MSL | WGSL |
|------|------|-----|------|
| `float2` | `vec2` | `float2` | `vec2<f32>` |
| `float3` | `vec3` | `float3` | `vec3<f32>` |
| `float4` | `vec4` | `float4` | `vec4<f32>` |
| `int2` | `ivec2` | `int2` | `vec2<i32>` |
| `int3` | `ivec3` | `int3` | `vec3<i32>` |
| `int4` | `ivec4` | `int4` | `vec4<i32>` |
| `uint2` | `uvec2` | `uint2` | `vec2<u32>` |
| `uint3` | `uvec3` | `uint3` | `vec3<u32>` |
| `uint4` | `uvec4` | `uint4` | `vec4<u32>` |
| `bool2` | `bvec2` | `bool2` | `vec2<bool>` |
| `bool3` | `bvec3` | `bool3` | `vec3<bool>` |
| `bool4` | `bvec4` | `bool4` | `vec4<bool>` |

### Matrix Types

| HLSL | GLSL | MSL | WGSL |
|------|------|-----|------|
| `float2x2` | `mat2` | `float2x2` | `mat2x2<f32>` |
| `float3x3` | `mat3` | `float3x3` | `mat3x3<f32>` |
| `float4x4` | `mat4` | `float4x4` | `mat4x4<f32>` |
| `float2x3` | `mat2x3` | `float2x3` | `mat2x3<f32>` |
| `float3x2` | `mat3x2` | `float3x2` | `mat3x2<f32>` |
| `float3x4` | `mat3x4` | `float3x4` | `mat3x4<f32>` |
| `float4x3` | `mat4x3` | `float4x3` | `mat4x3<f32>` |

### Texture/Sampler Types

| HLSL | GLSL | MSL | WGSL |
|------|------|-----|------|
| `Texture1D` | `sampler1D` | `texture1d<float>` | `texture_1d<f32>` |
| `Texture2D` | `sampler2D` | `texture2d<float>` | `texture_2d<f32>` |
| `Texture3D` | `sampler3D` | `texture3d<float>` | `texture_3d<f32>` |
| `TextureCube` | `samplerCube` | `texturecube<float>` | `texture_cube<f32>` |
| `Texture2DArray` | `sampler2DArray` | `texture2d_array<float>` | `texture_2d_array<f32>` |
| `RWTexture2D<float4>` | `image2D` | `texture2d<float,access::write>` | `texture_storage_2d<rgba32float,write>` |

---

## Intrinsic Functions

### Math Functions

| Operation | HLSL | GLSL | MSL | WGSL |
|-----------|------|------|-----|------|
| Absolute | `abs(x)` | `abs(x)` | `abs(x)` | `abs(x)` |
| Sign | `sign(x)` | `sign(x)` | `sign(x)` | `sign(x)` |
| Floor | `floor(x)` | `floor(x)` | `floor(x)` | `floor(x)` |
| Ceil | `ceil(x)` | `ceil(x)` | `ceil(x)` | `ceil(x)` |
| Round | `round(x)` | `round(x)` | `round(x)` | `round(x)` |
| Fractional | `frac(x)` | `fract(x)` | `fract(x)` | `fract(x)` |
| Modulo | `fmod(a,b)` | `mod(a,b)` | `fmod(a,b)` | `a % b` |
| Min | `min(a,b)` | `min(a,b)` | `min(a,b)` | `min(a,b)` |
| Max | `max(a,b)` | `max(a,b)` | `max(a,b)` | `max(a,b)` |
| Clamp | `clamp(x,a,b)` | `clamp(x,a,b)` | `clamp(x,a,b)` | `clamp(x,a,b)` |
| Saturate | `saturate(x)` | `clamp(x,0,1)` | `saturate(x)` | `clamp(x,0.0,1.0)` |
| Linear interp | `lerp(a,b,t)` | `mix(a,b,t)` | `mix(a,b,t)` | `mix(a,b,t)` |
| Smoothstep | `smoothstep(a,b,x)` | `smoothstep(a,b,x)` | `smoothstep(a,b,x)` | `smoothstep(a,b,x)` |
| Square root | `sqrt(x)` | `sqrt(x)` | `sqrt(x)` | `sqrt(x)` |
| Inverse sqrt | `rsqrt(x)` | `inversesqrt(x)` | `rsqrt(x)` | `inverseSqrt(x)` |
| Power | `pow(x,y)` | `pow(x,y)` | `pow(x,y)` | `pow(x,y)` |
| Exp | `exp(x)` | `exp(x)` | `exp(x)` | `exp(x)` |
| Log | `log(x)` | `log(x)` | `log(x)` | `log(x)` |
| Log2 | `log2(x)` | `log2(x)` | `log2(x)` | `log2(x)` |
| Reciprocal | `rcp(x)` | `1.0/x` | `rcp(x)` | `1.0/x` |
| Mad | `mad(a,b,c)` | `fma(a,b,c)` | `fma(a,b,c)` | `fma(a,b,c)` |

### Trigonometric Functions

| Operation | HLSL | GLSL | MSL | WGSL |
|-----------|------|------|-----|------|
| Sin | `sin(x)` | `sin(x)` | `sin(x)` | `sin(x)` |
| Cos | `cos(x)` | `cos(x)` | `cos(x)` | `cos(x)` |
| Tan | `tan(x)` | `tan(x)` | `tan(x)` | `tan(x)` |
| Asin | `asin(x)` | `asin(x)` | `asin(x)` | `asin(x)` |
| Acos | `acos(x)` | `acos(x)` | `acos(x)` | `acos(x)` |
| Atan2 | `atan2(y,x)` | `atan(y,x)` | `atan2(y,x)` | `atan2(y,x)` |
| SinCos | `sincos(x,s,c)` | `s=sin(x);c=cos(x)` | `sincos(x,s,c)` | `s=sin(x);c=cos(x)` |
| Degrees | `degrees(x)` | `degrees(x)` | `degrees(x)` | `degrees(x)` |
| Radians | `radians(x)` | `radians(x)` | `radians(x)` | `radians(x)` |

### Derivative Functions

| Operation | HLSL | GLSL | MSL | WGSL |
|-----------|------|------|-----|------|
| Derivative X | `ddx(x)` | `dFdx(x)` | `dfdx(x)` | `dpdx(x)` |
| Derivative Y | `ddy(x)` | `dFdy(x)` | `dfdy(x)` | `dpdy(x)` |
| Fwidth | `fwidth(x)` | `fwidth(x)` | `fwidth(x)` | `fwidth(x)` |

### Vector/Matrix Operations

| Operation | HLSL | GLSL | MSL | WGSL |
|-----------|------|------|-----|------|
| Dot | `dot(a,b)` | `dot(a,b)` | `dot(a,b)` | `dot(a,b)` |
| Cross | `cross(a,b)` | `cross(a,b)` | `cross(a,b)` | `cross(a,b)` |
| Normalize | `normalize(v)` | `normalize(v)` | `normalize(v)` | `normalize(v)` |
| Length | `length(v)` | `length(v)` | `length(v)` | `length(v)` |
| Distance | `distance(a,b)` | `distance(a,b)` | `distance(a,b)` | `distance(a,b)` |
| Reflect | `reflect(i,n)` | `reflect(i,n)` | `reflect(i,n)` | `reflect(i,n)` |
| Refract | `refract(i,n,r)` | `refract(i,n,r)` | `refract(i,n,r)` | `refract(i,n,r)` |
| Transpose | `transpose(m)` | `transpose(m)` | `transpose(m)` | `transpose(m)` |
| Determinant | `determinant(m)` | `determinant(m)` | `determinant(m)` | `determinant(m)` |
| Inverse | `inverse(m)` | `inverse(m)` | `inverse(m)` | `inverse(m)` |

### Texture Sampling

| Operation | HLSL | GLSL | MSL | WGSL |
|-----------|------|------|-----|------|
| Sample | `tex.Sample(s,uv)` | `texture(tex,uv)` | `tex.sample(s,uv)` | `textureSample(tex,s,uv)` |
| Sample LOD | `tex.SampleLevel(s,uv,lod)` | `textureLod(tex,uv,lod)` | `tex.sample(s,uv,level(lod))` | `textureSampleLevel(tex,s,uv,lod)` |
| Sample Grad | `tex.SampleGrad(s,uv,dx,dy)` | `textureGrad(tex,uv,dx,dy)` | `tex.sample(s,uv,gradient2d(dx,dy))` | `textureSampleGrad(tex,s,uv,dx,dy)` |
| Fetch | `tex.Load(pos)` | `texelFetch(tex,pos,lod)` | `tex.read(pos)` | `textureLoad(tex,pos)` |
| Store | `tex[pos] = val` | `imageStore(img,pos,val)` | `tex.write(val,pos)` | `textureStore(tex,pos,val)` |
| Size | `tex.GetDimensions(w,h)` | `textureSize(tex,lod)` | `tex.get_width()` | `textureDimensions(tex)` |

### Bit/Cast Functions

| Operation | HLSL | GLSL | MSL | WGSL |
|-----------|------|------|-----|------|
| As float | `asfloat(x)` | `intBitsToFloat(x)` | `as_type<float>(x)` | `bitcast<f32>(x)` |
| As int | `asint(x)` | `floatBitsToInt(x)` | `as_type<int>(x)` | `bitcast<i32>(x)` |
| As uint | `asuint(x)` | `floatBitsToUint(x)` | `as_type<uint>(x)` | `bitcast<u32>(x)` |
| Count bits | `countbits(x)` | `bitCount(x)` | `popcount(x)` | `countTrailingZeros(x)` |
| Reverse bits | `reversebits(x)` | `bitfieldReverse(x)` | `reverse_bits(x)` | `reverseBits(x)` |

---

## Semantic Mapping

### Vertex Shader Semantics

| Meaning | HLSL | GLSL | MSL | WGSL |
|---------|------|------|-----|------|
| Position output | `SV_Position` | `gl_Position` | `[[position]]` | `@builtin(position)` |
| Position input | `POSITION` | `layout(location=0) in` | `[[attribute(0)]]` | `@location(0)` |
| Normal | `NORMAL` | `layout(location=N) in` | `[[attribute(N)]]` | `@location(N)` |
| Vertex ID | `SV_VertexID` | `gl_VertexID` | `[[vertex_id]]` | `@builtin(vertex_index)` |
| Instance ID | `SV_InstanceID` | `gl_InstanceID` | `[[instance_id]]` | `@builtin(instance_index)` |

### Fragment Shader Semantics

| Meaning | HLSL | GLSL | MSL | WGSL |
|---------|------|------|-----|------|
| Color output | `SV_Target` | `layout(location=0) out` | `[[color(0)]]` | `@location(0)` |
| Depth output | `SV_Depth` | `gl_FragDepth` | `[[depth(any)]]` | `@builtin(frag_depth)` |
| Front facing | `SV_IsFrontFace` | `gl_FrontFacing` | `[[front_facing]]` | `@builtin(front_facing)` |

### Compute Shader Semantics

| Meaning | HLSL | GLSL | MSL | WGSL |
|---------|------|------|-----|------|
| Global thread ID | `SV_DispatchThreadID` | `gl_GlobalInvocationID` | `[[thread_position_in_grid]]` | `@builtin(global_invocation_id)` |
| Local thread ID | `SV_GroupThreadID` | `gl_LocalInvocationID` | `[[thread_position_in_threadgroup]]` | `@builtin(local_invocation_id)` |
| Group ID | `SV_GroupID` | `gl_WorkGroupID` | `[[threadgroup_position_in_grid]]` | `@builtin(workgroup_id)` |

---

## Buffer Binding

### HLSL
```hlsl
cbuffer CameraBuffer : register(b0) { float4x4 View; float4x4 Proj; }
Texture2D diffuseTex : register(t0);
SamplerState linearSampler : register(s0);
RWStructuredBuffer<float> outputBuffer : register(u0);
```

### GLSL
```glsl
layout(std140, binding = 0) uniform CameraBuffer { mat4 View; mat4 Proj; };
layout(std430, binding = 0) buffer OutputBuffer { float data[]; };
uniform sampler2D diffuseTex;
```

### MSL
```metal
constant CameraBuffer& cam [[buffer(0)]];
texture2d<float> diffuseTex [[texture(0)]];
sampler linearSampler [[sampler(0)]];
device float* outputBuffer [[buffer(0)]];
```

### WGSL
```wgsl
@group(0) @binding(0) var<uniform> camera: CameraBuffer;
@group(0) @binding(1) var diffuseTex: texture_2d<f32>;
@group(0) @binding(2) var linearSampler: sampler;
@group(0) @binding(3) var<storage, read_write> outputBuffer: array<f32>;
```

---

## Complete Templates

### HLSL Vertex + Pixel Shader
```hlsl
cbuffer TransformBuffer : register(b0) {
    float4x4 World;
    float4x4 View;
    float4x4 Projection;
};

struct VSInput {
    float3 position : POSITION;
    float3 normal : NORMAL;
    float2 texcoord : TEXCOORD0;
};

struct VSOutput {
    float4 position : SV_Position;
    float3 normal : NORMAL;
    float2 texcoord : TEXCOORD0;
};

VSOutput VSMain(VSInput input) {
    VSOutput output;
    float4 worldPos = mul(float4(input.position, 1.0), World);
    output.position = mul(mul(worldPos, View), Projection);
    output.normal = mul(input.normal, (float3x3)World);
    output.texcoord = input.texcoord;
    return output;
}

Texture2D diffuseTex : register(t0);
SamplerState sampler0 : register(s0);

float4 PSMain(VSOutput input) : SV_Target {
    return diffuseTex.Sample(sampler0, input.texcoord);
}
```

### HLSL Compute Shader
```hlsl
RWTexture2D<float4> OutputTex : register(u0);
Texture2D<float4> InputTex : register(t0);

[numthreads(8, 8, 1)]
void CSMain(uint3 id : SV_DispatchThreadID) {
    uint width, height;
    InputTex.GetDimensions(width, height);
    if (id.x >= width || id.y >= height) return;
    
    float4 color = InputTex[id.xy];
    float gray = dot(color.rgb, float3(0.299, 0.587, 0.114));
    OutputTex[id.xy] = float4(gray, gray, gray, color.a);
}
```

### GLSL Vertex + Fragment Shader
```glsl
#version 450

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;
layout(location = 2) in vec2 texcoord;

layout(location = 0) out vec3 v_normal;
layout(location = 1) out vec2 v_texcoord;

layout(std140, binding = 0) uniform TransformBuffer {
    mat4 World;
    mat4 View;
    mat4 Projection;
};

void main() {
    vec4 worldPos = World * vec4(position, 1.0);
    gl_Position = Projection * View * worldPos;
    v_normal = mat3(World) * normal;
    v_texcoord = texcoord;
}

// Fragment Shader
#version 450

layout(location = 0) in vec3 v_normal;
layout(location = 1) in vec2 v_texcoord;
layout(location = 0) out vec4 fragColor;

layout(binding = 0) uniform sampler2D diffuseTex;

void main() {
    fragColor = texture(diffuseTex, v_texcoord);
}
```

### MSL Vertex + Fragment Shader
```metal
#include <metal_stdlib>
using namespace metal;

struct VSInput {
    float4 position [[attribute(0)]];
    float3 normal [[attribute(1)]];
    float2 texcoord [[attribute(2)]];
};

struct VSOutput {
    float4 position [[position]];
    float3 normal;
    float2 texcoord;
};

struct TransformBuffer {
    float4x4 World;
    float4x4 View;
    float4x4 Projection;
};

vertex VSOutput vertex_main(
    VSInput input [[stage_in]],
    constant TransformBuffer& transform [[buffer(0)]]
) {
    VSOutput output;
    float4 worldPos = transform.World * input.position;
    output.position = transform.Projection * transform.View * worldPos;
    output.normal = (transform.World * float4(input.normal, 0.0)).xyz;
    output.texcoord = input.texcoord;
    return output;
}

fragment float4 fragment_main(
    VSOutput input [[stage_in]],
    texture2d<float> diffuseTex [[texture(0)]],
    sampler sampler0 [[sampler(0)]]
) {
    return diffuseTex.sample(sampler0, input.texcoord);
}
```

### WGSL Vertex + Fragment Shader
```wgsl
struct VSInput {
    @location(0) position: vec3<f32>,
    @location(1) normal: vec3<f32>,
    @location(2) texcoord: vec2<f32>,
}

struct VSOutput {
    @builtin(position) position: vec4<f32>,
    @location(0) normal: vec3<f32>,
    @location(1) texcoord: vec2<f32>,
}

struct TransformBuffer {
    World: mat4x4<f32>,
    View: mat4x4<f32>,
    Projection: mat4x4<f32>,
}

@group(0) @binding(0) var<uniform> transform: TransformBuffer;

@vertex
fn vs_main(input: VSInput) -> VSOutput {
    var output: VSOutput;
    let worldPos = transform.World * vec4<f32>(input.position, 1.0);
    output.position = transform.Projection * transform.View * worldPos;
    output.normal = (transform.World * vec4<f32>(input.normal, 0.0)).xyz;
    output.texcoord = input.texcoord;
    return output;
}

@group(0) @binding(1) var diffuseTex: texture_2d<f32>;
@group(0) @binding(2) var sampler0: sampler;

@fragment
fn fs_main(input: VSOutput) -> @location(0) vec4<f32> {
    return textureSample(diffuseTex, sampler0, input.texcoord);
}
```

---

## ReShade FX Reference

ReShade FX is based on DX9-style HLSL with extensions for post-processing effects.

### Preprocessor Macros

| Macro | Description |
|-------|-------------|
| `__FILE__` | Current file path |
| `__FILE_NAME__` | Current file name without path |
| `__FILE_STEM__` | Current file name without extension and path |
| `__LINE__` | Current line number |
| `__RESHADE__` | ReShade version (MAJOR*10000 + MINOR*100 + REVISION) |
| `__APPLICATION__` | 32-bit Fnv1a hash of executable name |
| `__VENDOR__` | GPU vendor ID (0x10de=NVIDIA, 0x1002=AMD, 0x8086=Intel) |
| `__DEVICE__` | Device ID |
| `__RENDERER__` | Graphics API (0x9000=D3D9, 0xa000=D3D10, 0xb000=D3D11, 0xc000=D3D12, 0x10000=OpenGL, 0x20000=Vulkan) |
| `BUFFER_WIDTH` | Backbuffer width in pixels |
| `BUFFER_HEIGHT` | Backbuffer height in pixels |
| `BUFFER_RCP_WIDTH` | Reciprocal width (1.0 / BUFFER_WIDTH) |
| `BUFFER_RCP_HEIGHT` | Reciprocal height (1.0 / BUFFER_HEIGHT) |
| `BUFFER_COLOR_FORMAT` | Backbuffer texture format |
| `BUFFER_COLOR_BIT_DEPTH` | Color bit depth (8, 10, or 16) |
| `BUFFER_COLOR_SPACE` | Color space (0=unknown, 1=sRGB, 2=scRGB, 3=HDR10 ST2084, 4=HDR10 HLG) |
| `ADDON_[NAME]` | Defined for each enabled addon (e.g., `ADDON_GENERIC_DEPTH`) |

```hlsl
// Prevent preprocessor defines from appearing in UI (prefix with underscore or <8 chars)
#ifndef _INTERNAL_DEFINE
    #define _INTERNAL_DEFINE 0
#endif

// Disable shader optimization for debugging
#pragma reshade skipoptimization
```

### Special Texture Semantics

```hlsl
texture2D texColor : COLOR;   // Backbuffer contents (read-only)
texture2D texDepth : DEPTH;   // Game's depth buffer (read-only)
```

### Texture Declaration

```hlsl
texture2D texTarget
{
    Width = BUFFER_WIDTH / 2;   // Default: 1
    Height = BUFFER_HEIGHT / 2; // Default: 1
    MipLevels = 1;              // Default: 1
    Format = RGBA8;             // Default: RGBA8
    // Available: R8, R16, R16F, R32F, R32I, R32U
    //            RG8, RG16, RG16F, RG32F
    //            RGBA8, RGBA16, RGBA16F, RGBA32F
    //            RGB10A2, R11G11B10F
};

// Load image from file
texture2D imageTex < source = "path/to/image.png"; > { Width = 512; Height = 512; };

// Pooled textures (memory sharing)
texture2D myTex1 < pooled = true; > { Width = 100; Height = 100; Format = RGBA8; };
```

### Sampler Declaration

```hlsl
sampler2D samplerColor
{
    Texture = texColor;       // Required: texture to sample
    AddressU = CLAMP;         // CLAMP, MIRROR, WRAP, BORDER
    AddressV = CLAMP;
    AddressW = CLAMP;
    MagFilter = LINEAR;       // POINT, LINEAR, ANISOTROPIC
    MinFilter = LINEAR;
    MipFilter = LINEAR;
    MinLOD = 0.0f;
    MaxLOD = 1000.0f;
    MipLODBias = 0.0f;
    SRGBTexture = false;      // Convert to linear on sample
};

// Access backbuffer via ReShade namespace
sampler2D BackBuffer { Texture = ReShade::BackBuffer; };
```

### Storage Objects (Compute Shaders)

```hlsl
storage2D storageTarget
{
    Texture = texTarget;
    MipLevel = 0;
};

// Integer storage
storage3D<int> storageVolume { Texture = texIntegerVolume; };
```

### Uniform Variables with UI Annotations

```hlsl
// Slider
uniform float Brightness <
    ui_type = "slider";
    ui_min = -1.0; ui_max = 1.0;
    ui_label = "Brightness";
    ui_tooltip = "Adjusts overall brightness";
    ui_units = "cd/m²";
> = 0.0;

// Drag (similar to slider)
uniform float Intensity <
    ui_type = "drag";
    ui_min = 0.0; ui_max = 2.0;
    ui_step = 0.01;
> = 1.0;

// Combo box
uniform int BlendMode <
    ui_type = "combo";
    ui_items = "Normal\0Multiply\0Screen\0Overlay\0";
    ui_label = "Blend Mode";
> = 0;

// Radio buttons
uniform int Quality <
    ui_type = "radio";
    ui_items = "Low\0Medium\0High\0Ultra\0";
> = 1;

// Color picker
uniform float3 TintColor <
    ui_type = "color";
    ui_label = "Tint Color";
> = float3(1.0, 1.0, 1.0);

// Button
uniform bool ResetSettings <
    ui_type = "button";
    ui_label = "Reset to Defaults";
> = false;

// Hidden from UI
uniform float4 InternalData < hidden = true; >;

// Read-only display
uniform float DebugValue < noedit = true; >;
```

### Runtime Value Sources

```hlsl
uniform float frametime < source = "frametime"; >;      // MS per frame
uniform int framecount < source = "framecount"; >;      // Total frames
uniform float4 date < source = "date"; >;               // (year, month, day, time)
uniform float timer < source = "timer"; >;              // MS since start

// Ping-pong animation
uniform float2 pingpong < source = "pingpong"; min = 0; max = 10; step = 2; smoothing = 0.0; >;

// Random value
uniform int random_value < source = "random"; min = 0; max = 10; >;

// Key input
uniform bool space_bar < source = "key"; keycode = 0x20; mode = ""; >;  // mode: "", "press", "toggle"

// Mouse input
uniform bool left_click < source = "mousebutton"; keycode = 0; >;
uniform float2 mouse_pos < source = "mousepoint"; >;
uniform float2 mouse_delta < source = "mousedelta"; >;
uniform float2 mouse_wheel < source = "mousewheel"; min = 0.0; max = 10.0; > = 1.0;

// State checks
uniform bool has_depth < source = "bufready_depth"; >;
uniform bool overlay_open < source = "overlay_open"; >;
uniform bool taking_screenshot < source = "screenshot"; >;
```

### Structs and Namespaces

```hlsl
struct VSOutput {
    float4 position : SV_Position;
    float2 texcoord : TEXCOORD0;
    float3 color : COLOR0;
};

namespace MyEffects {
    namespace Utils {
        float3 RGBtoHSV(float3 rgb) { return rgb; }
    }
    float3 ProcessColor(float3 color) { return Utils::RGBtoHSV(color); }
}
// Usage: MyEffects::ProcessColor(color)
```

### Vertex Shader (Full-Screen Quad)

```hlsl
// Standard ReShade vertex shader (provided by ReShade.fxh)
void PostProcessVS(in uint id : SV_VertexID, out float4 position : SV_Position, out float2 texcoord : TEXCOORD) {
    texcoord.x = (id == 2) ? 2.0 : 0.0;
    texcoord.y = (id == 1) ? 2.0 : 0.0;
    position = float4(texcoord * float2(2, -2) + float2(-1, 1), 0, 1);
}

// Alternative with shader attribute
[shader("vertex")]
void MyVS(uint id : SV_VertexID, out float4 position : SV_Position, out float2 texcoord : TEXCOORD0) {
    // Same logic
}
```

### Pixel Shader

```hlsl
// Basic pixel shader
float3 PS_Effect(float4 vpos : SV_Position, float2 texcoord : TEXCOORD) : SV_Target {
    float3 color = tex2D(ReShade::BackBuffer, texcoord).rgb;
    return color;
}

// With shader attribute
[shader("pixel")]
void PS_Effect2(float4 vpos : SV_Position, float2 texcoord : TEXCOORD0, out float4 color : SV_Target) {
    color = tex2D(ReShade::BackBuffer, texcoord);
}

// Using discard to exclude pixels
float4 PS_DiscardExample(float4 vpos : SV_Position, float2 texcoord : TEXCOORD) : SV_Target {
    if (texcoord.x < 0.1 || texcoord.x > 0.9)
        discard;  // Abort rendering this pixel
    return tex2D(ReShade::BackBuffer, texcoord);
}
```

### Function Parameter Qualifiers

```hlsl
// in: input parameter (default, implicit)
void ProcessInput(in float3 color) { }

// out: output parameter - value filled by function
void GetUV(out float2 uv) { uv = float2(0.5, 0.5); }

// inout: both input and output
void ModifyColor(inout float3 color) { color *= 0.5; }
```

### Flow Control Attributes

```hlsl
// Branch attributes
[branch] if (condition) { }     // Force dynamic branching
[flatten] if (condition) { }    // Force flatten (no branch)

// Switch attributes
[flatten] switch (value) { }
[branch] switch (value) { }
[forcecase] switch (value) { }
[call] switch (value) { }

// Loop attributes
[unroll] for (int i = 0; i < 4; i++) { }  // Unroll loop
[loop] for (int i = 0; i < n; i++) { }    // Don't unroll
[fastopt] for (int i = 0; i < n; i++) { } // Fast optimization
```

### Compute Shader

```hlsl
groupshared int sharedMem[64];

[numthreads(8, 8, 1)]
void CS_Main(uint3 id : SV_DispatchThreadID, uint3 tid : SV_GroupThreadID) {
    // Use tex2Dstore() for writing
    tex2Dstore(storageTarget, id.xy, float4(1, 0, 0, 1));
}
```

### Technique & Pass Definition

```hlsl
technique MyEffect <
    ui_label = "My Cool Effect";
    ui_tooltip = "Description shown on hover";
    enabled = true;              // Enable by default
    enabled_in_screenshot = true;
    hidden = false;              // Show in UI
    timeout = 0;                 // Auto-disable after MS (0 = never)
>
{
    pass p0
    {
        // Primitive topology for draw call
        PrimitiveTopology = TRIANGLELIST;  // POINTLIST, LINELIST, LINESTRIP, TRIANGLELIST, TRIANGLESTRIP
        VertexCount = 3;                   // Number of vertices ReShade generates

        // Shaders
        VertexShader = PostProcessVS;
        PixelShader = PS_Effect;

        // Render targets
        RenderTarget = texTarget;        // or RenderTarget0, RenderTarget1-7
        ClearRenderTargets = false;
        GenerateMipMaps = true;

        // Blend state
        BlendEnable = false;
        BlendOp = ADD;                   // ADD, SUBTRACT, REVSUBTRACT, MIN, MAX
        BlendOpAlpha = ADD;
        SrcBlend = ONE;                  // ZERO, ONE, SRCCOLOR, SRCALPHA, INVSRCCOLOR, INVSRCALPHA
        SrcBlendAlpha = ONE;
        DestBlend = ZERO;                // ZERO, ONE, DESTCOLOR, DESTALPHA, INVDESTCOLOR, INVDESTALPHA
        DestBlendAlpha = ZERO;

        // Stencil state
        StencilEnable = false;
        StencilRef = 0;
        StencilReadMask = 0xFF;          // 0-255
        StencilWriteMask = 0xFF;
        StencilFunc = ALWAYS;            // NEVER, ALWAYS, EQUAL, NOTEQUAL, LESS, GREATER, LESSEQUAL, GREATEREQUAL
        StencilPassOp = KEEP;            // KEEP, ZERO, REPLACE, INCR, INCRSAT, DECR, DECRSAT, INVERT
        StencilFailOp = KEEP;
        StencilDepthFailOp = KEEP;       // or StencilZFail

        // Output
        SRGBWriteEnable = false;
        RenderTargetWriteMask = 0xF;     // ColorWriteEnable
    }

    pass compute_pass
    {
        ComputeShader = CS_Main<8,8,1>;   // Thread group size
        DispatchSizeX = 20;               // 20 * 8 = 160 threads in X
        DispatchSizeY = 2;                // 2 * 8 = 16 threads in Y
        DispatchSizeZ = 1;
    }
}
```

#### Pass State Reference

| State | Values | Description |
|-------|--------|-------------|
| `PrimitiveTopology` | POINTLIST, LINELIST, LINESTRIP, TRIANGLELIST, TRIANGLESTRIP | Primitive type |
| `VertexCount` | 1-N | Number of vertices generated |
| `VertexShader` | function name | Vertex shader entry point |
| `PixelShader` | function name | Pixel shader entry point |
| `ComputeShader` | function<threads> | Compute shader with thread group size |
| `RenderTarget0-7` | texture name | Render target textures |
| `ClearRenderTargets` | true/false | Clear to zero before rendering |
| `GenerateMipMaps` | true/false | Auto-generate mipmaps after pass |
| `BlendEnable` | true/false | Enable blending |
| `BlendOp` | ADD, SUBTRACT, REVSUBTRACT, MIN, MAX | Color blend operation |
| `SrcBlend` | ZERO, ONE, SRCCOLOR, SRCALPHA, INVSRCCOLOR, INVSRCALPHA, DESTCOLOR, DESTALPHA, INVDESTCOLOR, INVDESTALPHA | Source blend factor |
| `DestBlend` | Same as SrcBlend | Destination blend factor |
| `StencilEnable` | true/false | Enable stencil test |
| `StencilFunc` | NEVER, ALWAYS, EQUAL, NOTEQUAL, LESS, GREATER, LESSEQUAL, GREATEREQUAL | Stencil comparison |
| `StencilPassOp` | KEEP, ZERO, REPLACE, INCR, INCRSAT, DECR, DECRSAT, INVERT | Stencil pass operation |
| `SRGBWriteEnable` | true/false | Apply gamma correction |
| `RenderTargetWriteMask` | 0x0-0xF | Color channel write mask |

### ReShade-Specific Intrinsics

#### Texture Sampling

```hlsl
// Basic sampling
T tex1D(sampler1D s, float coords)
T tex1D(sampler1D s, float coords, int offset)
T tex2D(sampler2D s, float2 coords)
T tex2D(sampler2D s, float2 coords, int2 offset)
T tex3D(sampler3D s, float3 coords)
T tex3D(sampler3D s, float3 coords, int3 offset)

// Sample at specific LOD
T tex1Dlod(sampler1D s, float4 coords)  // coords = float4(x, 0, 0, lod)
T tex2Dlod(sampler2D s, float4 coords)  // coords = float4(x, y, 0, lod)
T tex3Dlod(sampler3D s, float4 coords)  // coords = float4(x, y, z, lod)

// Sample with gradient (explicit derivatives)
T tex1Dgrad(sampler1D s, float coords, float ddx, float ddy)
T tex2Dgrad(sampler2D s, float2 coords, float2 ddx, float2 ddy)
T tex3Dgrad(sampler3D s, float3 coords, float3 ddx, float3 ddy)

// Fetch without filtering (integer coordinates)
T tex1Dfetch(sampler1D s, int coords)
T tex1Dfetch(sampler1D s, int coords, int lod)
T tex1Dfetch(storage1D s, int coords)
T tex2Dfetch(sampler2D s, int2 coords)
T tex2Dfetch(sampler2D s, int2 coords, int lod)
T tex2Dfetch(storage2D s, int2 coords)
T tex3Dfetch(sampler3D s, int3 coords)
T tex3Dfetch(sampler3D s, int3 coords, int lod)
T tex3Dfetch(storage3D s, int3 coords)

// Gather (returns 4 samples from neighboring pixels)
float4 tex2DgatherR(sampler2D s, float2 coords)  // Gather red component
float4 tex2DgatherG(sampler2D s, float2 coords)  // Gather green component
float4 tex2DgatherB(sampler2D s, float2 coords)  // Gather blue component
float4 tex2DgatherA(sampler2D s, float2 coords)  // Gather alpha component

// Get texture dimensions
int  tex1Dsize(sampler1D s)
int  tex1Dsize(sampler1D s, int lod)
int  tex1Dsize(storage1D s)
int2 tex2Dsize(sampler2D s)
int2 tex2Dsize(sampler2D s, int lod)
int2 tex2Dsize(storage2D s)
int3 tex3Dsize(sampler3D s)
int3 tex3Dsize(sampler3D s, int lod)
int3 tex3Dsize(storage3D s)

// Store to texture (compute only)
void tex1Dstore(storage1D s, int coords, T value)
void tex2Dstore(storage2D s, int2 coords, T value)
void tex3Dstore(storage3D s, int3 coords, T value)
```

#### Synchronization

```hlsl
void barrier()            // GroupMemoryBarrierWithGroupSync
void memoryBarrier()      // AllMemoryBarrier
void groupMemoryBarrier() // GroupMemoryBarrier
```

#### Atomic Operations

```hlsl
// All atomics return the original value before operation
int atomicAdd(inout int dest, int value)
int atomicAdd(storage1D s, int coords, int value)
int atomicAdd(storage2D s, int2 coords, int value)
int atomicAdd(storage3D s, int3 coords, int value)

int atomicAnd(inout int dest, int value)
int atomicOr(inout int dest, int value)
int atomicXor(inout int dest, int value)
int atomicMin(inout int dest, int value)
int atomicMax(inout int dest, int value)
int atomicExchange(inout int dest, int value)
int atomicCompareExchange(inout int dest, int compare, int value)
```

#### ReShade Built-in Samplers

```hlsl
ReShade::BackBuffer  // Game's rendered image
ReShade::DepthBuffer // Game's depth buffer
```

### ReShade Standard Library Headers

#### ReShade.fxh - Core Header

```hlsl
#include "ReShade.fxh"

// Provides:
// - Version checking: __RESHADE__ >= 30000
// - Buffer size macros: BUFFER_WIDTH, BUFFER_HEIGHT, BUFFER_RCP_WIDTH, BUFFER_RCP_HEIGHT
// - BUFFER_PIXEL_SIZE, BUFFER_SCREEN_SIZE, BUFFER_ASPECT_RATIO
// - ReShade::AspectRatio, ReShade::PixelSize, ReShade::ScreenSize
// - ReShade::BackBuffer, ReShade::DepthBuffer samplers
// - ReShade::GetLinearizedDepth(texcoord) helper
// - PostProcessVS() - standard fullscreen triangle vertex shader
```

#### ReShadeUI.fxh - UI Widget Types

```hlsl
#include "ReShadeUI.fxh"

// Version checking
#define RESHADE_VERSION(major,minor,build) (10000 * (major) + 100 * (minor) + (build))
#define SUPPORTED_VERSION(major,minor,build) (__RESHADE__ >= RESHADE_VERSION(major,minor,build))

// UI type macros (version-aware, work across ReShade 3.x/4.x/5.x)
// __UNIFORM_INPUT_FLOAT1, __UNIFORM_SLIDER_FLOAT1, __UNIFORM_DRAG_FLOAT1
// __UNIFORM_COMBO_INT1, __UNIFORM_RADIO_INT1, __UNIFORM_COLOR_FLOAT3
// __UNIFORM_LIST_INT1 (ReShade 4.3+)

// Example usage:
uniform float MyValue < __UNIFORM_SLIDER_FLOAT1
    ui_min = 0.0; ui_max = 1.0;
    ui_label = "My Value";
> = 0.5;

uniform int MyChoice < __UNIFORM_COMBO_INT1
    ui_items = "Option A\0Option B\0Option C\0";
    ui_label = "Choice";
> = 0;
```

### Depth Buffer Handling

#### Depth Configuration Defines

```hlsl
// These can be set in ReShade preprocessor settings or defined before including ReShade.fxh
#ifndef RESHADE_DEPTH_INPUT_IS_UPSIDE_DOWN
    #define RESHADE_DEPTH_INPUT_IS_UPSIDE_DOWN 0
#endif
#ifndef RESHADE_DEPTH_INPUT_IS_REVERSED
    #define RESHADE_DEPTH_INPUT_IS_REVERSED 1    // 1 = reversed depth (1=near, 0=far)
#endif
#ifndef RESHADE_DEPTH_INPUT_IS_LOGARITHMIC
    #define RESHADE_DEPTH_INPUT_IS_LOGARITHMIC 0
#endif
#ifndef RESHADE_DEPTH_MULTIPLIER
    #define RESHADE_DEPTH_MULTIPLIER 1
#endif
#ifndef RESHADE_DEPTH_LINEARIZATION_FAR_PLANE
    #define RESHADE_DEPTH_LINEARIZATION_FAR_PLANE 1000.0
#endif

// Coordinate adjustments
#ifndef RESHADE_DEPTH_INPUT_Y_SCALE
    #define RESHADE_DEPTH_INPUT_Y_SCALE 1
#endif
#ifndef RESHADE_DEPTH_INPUT_X_SCALE
    #define RESHADE_DEPTH_INPUT_X_SCALE 1
#endif
```

#### Manual Depth Linearization

```hlsl
float GetLinearizedDepth(float2 texcoord) {
#if RESHADE_DEPTH_INPUT_IS_UPSIDE_DOWN
    texcoord.y = 1.0 - texcoord.y;
#endif
#if RESHADE_DEPTH_INPUT_IS_MIRRORED
    texcoord.x = 1.0 - texcoord.x;
#endif
    texcoord.x /= RESHADE_DEPTH_INPUT_X_SCALE;
    texcoord.y /= RESHADE_DEPTH_INPUT_Y_SCALE;
    
    float depth = tex2Dlod(ReShade::DepthBuffer, float4(texcoord, 0, 0)).x * RESHADE_DEPTH_MULTIPLIER;
    
#if RESHADE_DEPTH_INPUT_IS_LOGARITHMIC
    const float C = 0.01;
    depth = (exp(depth * log(C + 1.0)) - 1.0) / C;
#endif
#if RESHADE_DEPTH_INPUT_IS_REVERSED
    depth = 1.0 - depth;
#endif
    
    const float N = 1.0;
    depth /= RESHADE_DEPTH_LINEARIZATION_FAR_PLANE - depth * (RESHADE_DEPTH_LINEARIZATION_FAR_PLANE - N);
    
    return depth;
}

// ReShade.fxh provides: ReShade::GetLinearizedDepth(texcoord)
```

### Complete ReShade FX Template

```hlsl
#include "ReShade.fxh"

uniform float Intensity <
    ui_type = "slider";
    ui_min = 0.0; ui_max = 1.0;
    ui_label = "Effect Intensity";
    ui_tooltip = "Controls the strength of the effect";
> = 0.5;

texture2D texTemp { Width = BUFFER_WIDTH; Height = BUFFER_HEIGHT; Format = RGBA8; };
sampler2D samplerTemp { Texture = texTemp; };

float3 PS_Main(float4 vpos : SV_Position, float2 texcoord : TEXCOORD) : SV_Target {
    float3 original = tex2D(ReShade::BackBuffer, texcoord).rgb;
    float3 processed = original * Intensity;
    return processed;
}

technique MyEffect <
    ui_label = "My Effect";
    ui_tooltip = "A simple effect template";
>
{
    pass
    {
        VertexShader = PostProcessVS;
        PixelShader = PS_Main;
    }
}
```

### Common Post-Processing Techniques

#### Blending Modes

```hlsl
namespace Blending {
    // Darken
    float3 Darken(float3 a, float3 b) { return min(a, b); }
    float3 Multiply(float3 a, float3 b) { return a * b; }
    float3 ColorBurn(float3 a, float3 b) {
        return (b.r > 0 && b.g > 0 && b.b > 0) ? 1.0 - min(1.0, (0.5 - a) / b) : 0.0;
    }
    float3 LinearBurn(float3 a, float3 b) { return max(a + b - 1.0, 0.0); }
    
    // Lighten
    float3 Lighten(float3 a, float3 b) { return max(a, b); }
    float3 Screen(float3 a, float3 b) { return 1.0 - (1.0 - a) * (1.0 - b); }
    float3 ColorDodge(float3 a, float3 b) {
        return (b.r < 1 && b.g < 1 && b.b < 1) ? min(1.0, a / (1.0 - b)) : 1.0;
    }
    float3 LinearDodge(float3 a, float3 b) { return min(a + b, 1.0); }
    
    // Contrast
    float3 Overlay(float3 a, float3 b) {
        return lerp(2 * a * b, 1.0 - 2 * (1.0 - a) * (1.0 - b), step(0.5, a));
    }
    float3 SoftLight(float3 a, float3 b) {
        return clamp(a - (1.0 - 2 * b) * a * (1 - a), 0, 1);
    }
    float3 HardLight(float3 a, float3 b) {
        return lerp(2 * a * b, 1.0 - 2 * (1.0 - b) * (1.0 - a), step(0.5, b));
    }
    
    // Inversion
    float3 Difference(float3 a, float3 b) { return max(a - b, b - a); }
    float3 Exclusion(float3 a, float3 b) { return a + b - 2 * a * b; }
}
```

---

## Unity ShaderLab Reference

Unity uses ShaderLab, a declarative language that wraps HLSL/Cg code with additional Unity-specific features. File extension: `.shader`

### Shader Structure

```hlsl
Shader "Category/ShaderName"
{
    Properties
    {
        // Exposed properties visible in Inspector
    }
    
    SubShader
    {
        // GPU-specific rendering setup
        Pass
        {
            // Rendering pass
        }
    }
    
    FallBack "Diffuse"  // Optional fallback shader
}
```

### Properties Block

```hlsl
Properties
{
    // Basic types
    _Color ("Main Color", Color) = (1, 1, 1, 1)
    _MainTex ("Albedo (RGB)", 2D) = "white" {}
    _NormalMap ("Normal Map", 2D) = "bump" {}
    _Cutoff ("Alpha Cutoff", Range(0, 1)) = 0.5
    _Glossiness ("Smoothness", Range(0, 1)) = 0.5
    _Metallic ("Metallic", Range(0, 1)) = 0.0
    _EmissionColor ("Emission Color", Color) = (0, 0, 0, 1)
    
    // Advanced types
    _IntValue ("Integer", Int) = 1
    _FloatValue ("Float", Float) = 1.0
    _VectorValue ("Vector", Vector) = (1, 1, 1, 1)
    _CubeMap ("Environment Map", Cube) = "" {}
    _3DTex ("3D Texture", 3D) = "" {}
}
```

| Type | Syntax | Description |
|------|--------|-------------|
| `Color` | `Color` = (r, g, b, a) | Color picker in Inspector |
| `2D` | `2D` = "white" {} | 2D texture (white, black, gray, bump) |
| `3D` | `3D` = "" {} | 3D texture |
| `Cube` | `Cube` = "" {} | Cubemap texture |
| `Range` | `Range(min, max)` = default | Slider with min/max |
| `Float` | `Float` = default | Float input field |
| `Int` | `Int` = default | Integer input field |
| `Vector` | `Vector` = (x, y, z, w) | 4-component vector field |

### SubShader Block

```hlsl
SubShader
{
    // Render state setup
    Tags { "RenderType" = "Opaque" "Queue" = "Geometry" }
    LOD 200
    
    // Optional: Cull, ZWrite, ZTest, Blend, etc.
    Cull Back
    ZWrite On
    ZTest LEqual
    Blend SrcAlpha OneMinusSrcAlpha
    
    Pass
    {
        Name "BASE"  // Optional pass name
        Tags { "LightMode" = "ForwardBase" }
        
        // Per-pass state overrides
        Blend One One  // Additive blending for this pass
        
        CGPROGRAM
        // HLSL code here
        ENDCG
    }
}
```

### SubShader Tags

| Tag | Values | Description |
|-----|--------|-------------|
| `RenderType` | Opaque, Transparent, TransparentCutout, Background, Overlay | Shader replacement category |
| `Queue` | Background, Geometry, AlphaTest, Transparent, Overlay (+offset) | Render order |
| `IgnoreProjector` | True, False | Skip projector rendering |
| `ForceNoShadowCasting` | True, False | Disable shadow casting |
| `PreviewType` | Plane, Sphere, Skybox | Material preview shape |

```hlsl
Tags {
    "RenderType" = "Transparent"
    "Queue" = "Transparent+100"  // After standard transparent
    "IgnoreProjector" = "True"
    "ForceNoShadowCasting" = "True"
}
```

### Render State Commands

```hlsl
// Culling
Cull Back    // Default - cull back faces
Cull Front   // Cull front faces
Cull Off     // No culling (double-sided)

// Depth
ZWrite On    // Write to depth buffer
ZWrite Off   // Don't write to depth
ZTest LEqual // Default - pass if depth <= buffer
ZTest Greater
ZTest Less
ZTest Equal
ZTest Always

// Blending
Blend Off                                    // No blending
Blend SrcAlpha OneMinusSrcAlpha              // Standard alpha
Blend One One                                // Additive
Blend One OneMinusSrcAlpha                   // Premultiplied alpha
Blend DstColor Zero                          // Multiply
Blend SrcAlpha One                           // Soft additive
BlendOp Add                                  // Default blend operation

// Stencil
Stencil {
    Ref 1
    Comp Always
    Pass Replace
    Fail Keep
    ZFail Keep
}
```

### Pass Tags (LightMode)

| LightMode | Description |
|-----------|-------------|
| `Always` | Always rendered, regardless of lighting |
| `ForwardBase` | Main forward pass (main directional light, ambient, lightmaps) |
| `ForwardAdd` | Additional per-pixel lights (one pass per light) |
| `Deferred` | Deferred shading G-buffer pass |
| `ShadowCaster` | Shadow mapping pass |
| `Meta` | Lightmap baking pass |
| `MotionVectors` | Motion vector pass |

### Unity Shader Types

#### 1. Unlit Shader

```hlsl
Shader "Custom/UnlitExample"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _Color ("Color", Color) = (1, 1, 1, 1)
    }
    
    SubShader
    {
        Tags { "RenderType" = "Opaque" }
        
        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            
            #include "UnityCG.cginc"
            
            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
            };
            
            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };
            
            sampler2D _MainTex;
            float4 _MainTex_ST;
            float4 _Color;
            
            v2f vert(appdata v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.uv, _MainTex);
                return o;
            }
            
            fixed4 frag(v2f i) : SV_Target
            {
                return tex2D(_MainTex, i.uv) * _Color;
            }
            ENDCG
        }
    }
}
```

#### 2. Surface Shader

```hlsl
Shader "Custom/SurfaceExample"
{
    Properties
    {
        _Color ("Color", Color) = (1, 1, 1, 1)
        _MainTex ("Albedo (RGB)", 2D) = "white" {}
        _Glossiness ("Smoothness", Range(0, 1)) = 0.5
        _Metallic ("Metallic", Range(0, 1)) = 0.0
        _Emission ("Emission", Color) = (0, 0, 0, 1)
    }
    
    SubShader
    {
        Tags { "RenderType" = "Opaque" }
        LOD 200
        
        CGPROGRAM
        #pragma surface surf Standard fullforwardshadows
        #pragma target 3.0
        
        sampler2D _MainTex;
        
        struct Input
        {
            float2 uv_MainTex;
            float3 worldPos;      // Built-in: world position
            float3 viewDir;       // Built-in: view direction
            float3 worldNormal;   // Built-in: world normal
        };
        
        half _Glossiness;
        half _Metallic;
        fixed4 _Color;
        fixed4 _Emission;
        
        void surf(Input IN, inout SurfaceOutputStandard o)
        {
            fixed4 c = tex2D(_MainTex, IN.uv_MainTex) * _Color;
            o.Albedo = c.rgb;
            o.Metallic = _Metallic;
            o.Smoothness = _Glossiness;
            o.Alpha = c.a;
            o.Emission = _Emission.rgb;
        }
        ENDCG
    }
    FallBack "Diffuse"
}
```

#### Surface Output Structures

```hlsl
// Standard (PBR)
struct SurfaceOutputStandard
{
    fixed3 Albedo;      // Base color
    fixed3 Normal;      // Tangent space normal
    half3 Emission;     // Emissive color
    half Metallic;      // 0 = dielectric, 1 = metal
    half Smoothness;    // 0 = rough, 1 = smooth
    half Occlusion;     // Ambient occlusion
    fixed Alpha;        // Alpha for transparency
};

// Lambert
struct SurfaceOutput
{
    fixed3 Albedo;
    fixed3 Normal;
    fixed3 Emission;
    half Specular;
    fixed Gloss;
    fixed Alpha;
};
```

#### Surface Shader Directives

```hlsl
// Lighting models
#pragma surface surf Lambert     // Diffuse
#pragma surface surf BlinnPhong  // Specular
#pragma surface surf Standard    // PBR metallic
#pragma surface surf StandardSpecular  // PBR specular

// Optional parameters
#pragma surface surf Lambert alpha        // Alpha blending
#pragma surface surf Lambert vertex:vert // Custom vertex function
#pragma surface surf Lambert finalcolor:mycolor // Final color modifier
#pragma surface surf Lambert addshadow   // Generate shadow caster pass
#pragma surface surf Lambert fullforwardshadows // Support all light types
#pragma surface surf Lambert noambient   // No ambient light
#pragma surface surf Lambert novertexlights // No per-vertex lights
#pragma surface surf Lambert nolightmap  // No lightmaps

// Shader model targets
#pragma target 2.5   // Default
#pragma target 3.0   // Required for some features
#pragma target 4.5   // DX11 shader model 4.5
#pragma target 5.0   // DX11 shader model 5.0
```

### Built-in Include Files

```hlsl
#include "UnityCG.cginc"        // Common functions and macros
#include "UnityStandardCore.cginc"  // Standard shader core
#include "Lighting.cginc"       // Lighting functions
#include "AutoLight.cginc"      // Automatic lighting macros
#include "HLSLSupport.cginc"    // Platform compatibility
#include "UnityShaderVariables.cginc" // Built-in variables
```

### Unity Built-in Variables

#### Transform Matrices

```hlsl
float4x4 UNITY_MATRIX_MVP;      // Model * View * Projection
float4x4 UNITY_MATRIX_MV;       // Model * View
float4x4 UNITY_MATRIX_V;        // View matrix
float4x4 UNITY_MATRIX_P;        // Projection matrix
float4x4 UNITY_MATRIX_VP;       // View * Projection
float4x4 unity_ObjectToWorld;   // Model matrix (local to world)
float4x4 unity_WorldToObject;   // Inverse model matrix
```

#### Camera & Screen

```hlsl
float3 _WorldSpaceCameraPos;    // Camera position in world space
float4 _ProjectionParams;       // x = 1/-1 (normal/inverted), y = near, z = far, w = 1/far
float4 _ScreenParams;           // x = width, y = height, z = 1 + 1/width, w = 1 + 1/height
```

#### Time

```hlsl
float4 _Time;       // (t/20, t, t*2, t*3) - game time
float4 _SinTime;    // (sin(t/8), sin(t/4), sin(t/2), sin(t))
float4 _CosTime;    // (cos(t/8), cos(t/4), cos(t/2), cos(t))
float4 unity_DeltaTime; // (dt, 1/dt, smooth dt, 1/smooth dt)
```

#### Lighting

```hlsl
float4 _WorldSpaceLightPos0;    // Directional: (dir, 0), Point/Spot: (pos, 1)
float4 _LightColor0;            // RGB = color, A = intensity
float4 unity_AmbientSky;        // Sky ambient color
float4 unity_FogColor;          // Fog color
float4 unity_FogParams;         // Fog parameters
```

### Unity Built-in Functions

```hlsl
// Transform functions (UnityCG.cginc)
float3 UnityObjectToWorldNormal(float3 norm);    // Local normal to world
float3 UnityObjectToWorldDir(float3 dir);        // Local direction to world
float4 UnityObjectToClipPos(float3 pos);         // Local to clip space
float3 UnityViewToWorldDir(float3 dir);          // View to world direction

// Depth functions
float LinearEyeDepth(float rawDepth);            // Raw depth to eye depth
float Linear01Depth(float rawDepth);             // Raw depth to 0-1 linear

// UV functions
float2 TRANSFORM_TEX(float2 uv, sampler2D tex);  // Apply texture scale/offset

// Utility
float3 UnpackNormal(float4 packedNormal);        // Unpack normal map
float3 UnpackNormalWithScale(float4 packed, float scale); // With scale
```

### GrabPass

```hlsl
GrabPass
{
    "_BackgroundTexture"  // Store in named texture
}

// Later in another pass
sampler2D _BackgroundTexture;

fixed4 frag(v2f i) : SV_Target
{
    float2 uv = i.grabPos.xy / i.grabPos.w;
    fixed4 col = tex2D(_BackgroundTexture, uv);
    return col;
}
```

### Multi-Compile & Shader Variants

```hlsl
// Single keyword (on/off)
#pragma multi_compile FOG_ON FOG_OFF

// Built-in multi-compiles
#pragma multi_compile_fog           // Fog variants
#pragma multi_compile_instancing    // GPU instancing variants
#pragma multi_compile_fwdbase       // Forward base pass variants
#pragma multi_compile_fwdadd        // Forward add pass variants

// Usage in code
#ifdef FOG_ON
    color = lerp(color, unity_FogColor, fogFactor);
#endif
```

### GPU Instancing

```hlsl
Properties
{
    _Color ("Color", Color) = (1, 1, 1, 1)
}

SubShader
{
    Pass
    {
        CGPROGRAM
        #pragma vertex vert
        #pragma fragment frag
        #pragma multi_compile_instancing
        
        #include "UnityCG.cginc"
        
        struct appdata
        {
            float4 vertex : POSITION;
            UNITY_VERTEX_INPUT_INSTANCE_ID  // Required for instancing
        };
        
        UNITY_INSTANCING_BUFFER_START(Props)
            UNITY_DEFINE_INSTANCED_PROP(float4, _Color)
        UNITY_INSTANCING_BUFFER_END(Props)
        
        v2f vert(appdata v)
        {
            v2f o;
            UNITY_SETUP_INSTANCE_ID(v);
            UNITY_TRANSFER_INSTANCE_ID(v, o);
            o.vertex = UnityObjectToClipPos(v.vertex);
            return o;
        }
        
        fixed4 frag(v2f i) : SV_Target
        {
            UNITY_SETUP_INSTANCE_ID(i);
            return UNITY_ACCESS_INSTANCED_PROP(Props, _Color);
        }
        ENDCG
    }
}
```

### Unity Shader Best Practices

1. **Naming Convention**: Use `Category/Name` format (e.g., "Custom/Water")
2. **Organize shaders in dedicated folders** (e.g., `Assets/Shaders/`)
3. **Use `LOD` values** for level-of-detail fallback
4. **Test in different lighting conditions** (forward, deferred, vertex-lit)
5. **Consider mobile compatibility** - use `#pragma target 2.5` when possible
6. **Use `FallBack`** for older GPU support
7. **Profile shader performance** with Unity Frame Debugger
8. **Batch similar materials** using GPU instancing
9. **Avoid `discard`/`clip`** in mobile shaders (causes early-Z issues)
10. **Use texture atlases** to reduce draw calls

---

## WebGL Reference

WebGL (Web Graphics Library) is a JavaScript API for hardware-accelerated 2D and 3D graphics in web browsers, based on OpenGL ES.

### Context Initialization

```javascript
// WebGL 1.0
const canvas = document.querySelector("canvas");
const gl = canvas.getContext("webgl") || canvas.getContext("experimental-webgl");

// WebGL 2.0 (preferred)
const gl = canvas.getContext("webgl2");

if (!gl) {
    console.error("WebGL not supported");
}

// Context creation options
const gl = canvas.getContext("webgl2", {
    alpha: false,              // No alpha channel (better performance)
    antialias: true,           // Antialiasing
    depth: true,               // Depth buffer
    stencil: false,            // Stencil buffer
    premultipliedAlpha: true,  // Alpha premultiplication
    preserveDrawingBuffer: false, // Keep buffer after render
    powerPreference: "high-performance", // GPU preference
});
```

### WebGL Version Comparison

| Feature | WebGL 1.0 | WebGL 2.0 |
|---------|-----------|-----------|
| GLSL Version | GLSL ES 1.00 | GLSL ES 3.00 |
| Vertex Array Objects | Extension | Core |
| Instanced Rendering | Extension | Core |
| 3D Textures | ❌ | ✅ |
| Sampler Objects | ❌ | ✅ |
| Uniform Buffer Objects | ❌ | ✅ |
| Multiple Render Targets | Extension | Core |

### Shader Compilation Pipeline

```javascript
function createShader(gl, type, source) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        console.error("Shader compilation error:", gl.getShaderInfoLog(shader));
        gl.deleteShader(shader);
        return null;
    }
    return shader;
}

function createProgram(gl, vertexShader, fragmentShader) {
    const program = gl.createProgram();
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);
    gl.linkProgram(program);
    
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        console.error("Program linking error:", gl.getProgramInfoLog(program));
        gl.deleteProgram(program);
        return null;
    }
    return program;
}

// Usage
const vertexShader = createShader(gl, gl.VERTEX_SHADER, vsSource);
const fragmentShader = createShader(gl, gl.FRAGMENT_SHADER, fsSource);
const program = createProgram(gl, vertexShader, fragmentShader);
```

### WebGL GLSL Shaders

#### Basic Vertex Shader (GLSL ES 1.00)

```glsl
attribute vec3 aPosition;
attribute vec2 aTexCoord;
attribute vec3 aNormal;

uniform mat4 uModelMatrix;
uniform mat4 uViewMatrix;
uniform mat4 uProjectionMatrix;

varying vec3 vNormal;
varying vec2 vTexCoord;

void main() {
    vec4 worldPosition = uModelMatrix * vec4(aPosition, 1.0);
    gl_Position = uProjectionMatrix * uViewMatrix * worldPosition;
    vNormal = mat3(uModelMatrix) * aNormal;
    vTexCoord = aTexCoord;
}
```

#### Basic Fragment Shader (GLSL ES 1.00)

```glsl
precision mediump float;

varying vec3 vNormal;
varying vec2 vTexCoord;

uniform sampler2D uTexture;
uniform vec3 uLightPosition;
uniform vec3 uLightColor;

void main() {
    vec3 normal = normalize(vNormal);
    vec3 lightDir = normalize(uLightPosition);
    float diff = max(dot(normal, lightDir), 0.0);
    
    vec4 texColor = texture2D(uTexture, vTexCoord);
    vec3 result = diff * uLightColor * texColor.rgb;
    
    gl_FragColor = vec4(result, texColor.a);
}
```

#### WebGL 2.0 Fragment Shader (GLSL ES 3.00)

```glsl
#version 300 es
precision highp float;

in vec3 vNormal;
in vec2 vTexCoord;

uniform sampler2D uTexture;
uniform vec3 uLightColor;

out vec4 fragColor;

void main() {
    vec3 normal = normalize(vNormal);
    float diff = max(dot(normal, vec3(0.0, 1.0, 0.0)), 0.0);
    vec4 texColor = texture(uTexture, vTexCoord);
    fragColor = vec4(diff * uLightColor * texColor.rgb, texColor.a);
}
```

### Buffer Management

```javascript
// Create and populate a vertex buffer
const positionBuffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);

const positions = new Float32Array([
    -1.0, -1.0, 0.0,  // Vertex 1
     1.0, -1.0, 0.0,  // Vertex 2
     0.0,  1.0, 0.0   // Vertex 3
]);
gl.bufferData(gl.ARRAY_BUFFER, positions, gl.STATIC_DRAW);

// Buffer usage hints
// gl.STATIC_DRAW  - Data doesn't change
// gl.DYNAMIC_DRAW - Data changes occasionally
// gl.STREAM_DRAW  - Data changes every frame
```

### Vertex Attributes

```javascript
const positionLocation = gl.getAttribLocation(program, "aPosition");
gl.enableVertexAttribArray(positionLocation);
gl.vertexAttribPointer(
    positionLocation,  // Attribute location
    3,                 // Components per vertex (x, y, z)
    gl.FLOAT,          // Data type
    false,             // Normalize?
    0,                 // Stride (0 = tightly packed)
    0                  // Offset
);
```

### Texture Handling

```javascript
function createTexture(gl, image) {
    const texture = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, texture);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image);
    
    // Power-of-2 check
    if (isPowerOf2(image.width) && isPowerOf2(image.height)) {
        gl.generateMipmap(gl.TEXTURE_2D);
    } else {
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    }
    return texture;
}

// Texture filtering options
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
```

### Rendering Loop

```javascript
function render(time) {
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clearColor(0.0, 0.0, 0.0, 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    
    gl.enable(gl.DEPTH_TEST);
    gl.depthFunc(gl.LEQUAL);
    
    gl.useProgram(program);
    // Set uniforms and bind textures...
    gl.drawArrays(gl.TRIANGLES, 0, vertexCount);
    
    requestAnimationFrame(render);
}
```

### Vertex Array Objects (VAO) - WebGL 2

```javascript
// Create VAO
const vao = gl.createVertexArray();
gl.bindVertexArray(vao);

// Set up all vertex attributes
gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
gl.enableVertexAttribArray(positionLocation);
gl.vertexAttribPointer(positionLocation, 3, gl.FLOAT, false, 0, 0);

gl.bindVertexArray(null);

// In render loop
gl.bindVertexArray(vao);
gl.drawArrays(gl.TRIANGLES, 0, vertexCount);
```

### Framebuffer Rendering (Render to Texture)

```javascript
// Create framebuffer
const framebuffer = gl.createFramebuffer();
gl.bindFramebuffer(gl.FRAMEBUFFER, framebuffer);

// Create target texture
const targetTexture = gl.createTexture();
gl.bindTexture(gl.TEXTURE_2D, targetTexture);
gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, width, height, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);

// Attach texture to framebuffer
gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, targetTexture, 0);

// Create depth renderbuffer
const depthBuffer = gl.createRenderbuffer();
gl.bindRenderbuffer(gl.RENDERBUFFER, depthBuffer);
gl.renderbufferStorage(gl.RENDERBUFFER, gl.DEPTH_COMPONENT16, width, height);
gl.framebufferRenderbuffer(gl.FRAMEBUFFER, gl.DEPTH_ATTACHMENT, gl.RENDERBUFFER, depthBuffer);

// Check framebuffer status
if (gl.checkFramebufferStatus(gl.FRAMEBUFFER) !== gl.FRAMEBUFFER_COMPLETE) {
    console.error("Framebuffer incomplete");
}

// Render to framebuffer
gl.bindFramebuffer(gl.FRAMEBUFFER, framebuffer);
gl.viewport(0, 0, width, height);
// ... render scene ...

// Render to canvas
gl.bindFramebuffer(gl.FRAMEBUFFER, null);
gl.viewport(0, 0, canvas.width, canvas.height);
// ... use targetTexture ...
```

### Blend Functions

```javascript
// Standard alpha blending
gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

// Additive blending
gl.blendFunc(gl.SRC_ALPHA, gl.ONE);

// Premultiplied alpha
gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);

// Multiply
gl.blendFunc(gl.DST_COLOR, gl.ZERO);
```

### WebGL Extensions

```javascript
// Check for extension
const ext = gl.getExtension("OES_vertex_array_object");
if (ext) {
    const vao = ext.createVertexArrayOES();
}

// Common WebGL 1 extensions
gl.getExtension("ANGLE_instanced_arrays");        // Instanced rendering
gl.getExtension("OES_vertex_array_object");       // VAO support
gl.getExtension("OES_texture_float");             // Float textures
gl.getExtension("WEBGL_depth_texture");           // Depth textures
gl.getExtension("EXT_texture_filter_anisotropic"); // Anisotropic filtering
```

### Performance Targets

| Target | Frame Time | Draw Calls (Desktop) | Draw Calls (Mobile) |
|--------|------------|---------------------|---------------------|
| 60 FPS | 16.67ms | ~1000-5000 | ~100-500 |
| 30 FPS | 33.33ms | ~2000-10000 | ~200-1000 |

### Popular WebGL Libraries

| Library | Description |
|---------|-------------|
| **three.js** | Comprehensive 3D library with scene graph |
| **Babylon.js** | Game engine with physics and VR support |
| **Pixi.js** | Fast 2D WebGL renderer |
| **regl** | Functional WebGL wrapper |
| **twgl** | Tiny WebGL helper library |
| **glMatrix** | High-performance matrix/vector library |

---

## Performance Guidelines Summary

### Critical Optimizations

1. **Minimize texture samples** - Cache results, use atlases, batch similar operations
2. **Avoid dynamic branches** - Use `step()`, `mix()`, `min()/max()` instead of `if/else`
3. **Use appropriate precision** - `half`/`mediump` for colors, `float`/`highp` for positions
4. **Group uniforms in buffers** - Reduce binding changes, align to 16-byte boundaries
5. **Precompute in vertex shader** - Pass varyings to fragment when possible
6. **Avoid discard/kill** - Causes early-Z optimization failures on some GPUs
7. **Reduce overdraw** - Render front-to-back with depth testing
8. **Use mipmaps** - Improves texture cache hit rate for distant objects

### Transcendental Priority

| Optimization | Impact | Effort | Validation |
|--------------|--------|--------|------------|
| sin/cos → sincos | High | Low | ✅ Always safe |
| pow(x, 2.0) → x * x | High | Low | ✅ Always safe |
| pow(x, 3.0) → x * x * x | High | Low | ✅ Always safe |
| Hoist repeated calls | Medium-High | Medium | ✅ Always safe |
| sqrt(x) vs pow(x, 0.5) | Medium | Low | ✅ Always safe (x ≥ 0) |
| Taylor approximations | Varies | Medium | ⚠️ **Test required** |
