# GLSL Topic Map

Use this as a quick orientation aid when deciding what docs to look up.

## Core areas

- Language syntax, statements, and expressions
- Scalar/vector/matrix/array/struct types
- Storage, interpolation, memory, and layout qualifiers
- Inputs/outputs and stage interfaces
- Uniforms, buffers, samplers, images, and opaque types
- Built-in variables and built-in functions
- Preprocessor, versioning, and extensions
- Vertex, fragment, compute, geometry, tessellation, and ray-tracing stage usage where documented

## Typical lookup prompts

When the task is about...

### Syntax / types / qualifiers
Look for docs covering:
- types
- constructors
- storage qualifiers
- memory qualifiers
- layout qualifiers
- precision/version rules when relevant

### Interfaces / resources
Look for docs covering:
- stage inputs and outputs
- interface blocks
- uniforms
- shader storage blocks
- samplers and images

### Built-ins / stages / errors
Look for docs covering:
- built-in variables
- built-in functions
- stage-specific semantics
- preprocessor/version directives
- extension behavior
- compiler/validator error context

## Trigger boundary reminder

Use this skill for GLSL-specific language/spec/review/troubleshooting work.
Do not trigger it for generic graphics, SPIR-V assembly, or Vulkan API questions unless the actual issue is specifically about GLSL.
