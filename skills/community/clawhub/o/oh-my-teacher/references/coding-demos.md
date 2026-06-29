# Coding Demos

For interaction mode selection when coding (coding assistant vs. visual-first), see `references/interaction-modes.md`. For grading rubrics for code questions, see `references/question-types.md`. For host fallbacks, see `references/environment-adaptation.md`.

Use runnable demos to make abstract processes visible. Match the language and complexity to the user's course level.

## Before Writing Code

Infer or ask:

- Course language and allowed libraries
- Learned topics and forbidden advanced syntax
- Goal: understand concept, prepare coding exam, debug, simulate, visualize
- Runtime constraints if any

If unknown, default to simple Python for concept demos or basic C++ for C++ course review. Avoid advanced C++ features by default.

Before generating any demo, verify the host environment's tool availability:

- If you DO NOT have a python compiler/interpreter or shell tool in your actual available tool list, you MUST treat the environment as "plain-chat".
- In plain-chat, notes-app, or RAG-notebook environments, NEVER output commands like `plt.show()` that expect a GUI window.
- Always pair code with its expected output; the output itself is the primary teaching artifact, the code is for reference.
- If the user asks you to "run" the code but you have no execution tool, explain that you can only show the code and expected output, then offer a variant question.

## Demo Types

- Algorithm trace: sorting, recursion, BFS/DFS, dynamic programming, graph shortest path.
- Data structure state: stack, queue, heap, tree rotations, hash collisions.
- Math/physics simulation: numerical integration, probability simulation, matrix transforms, oscillation.
- Systems concept: process scheduling, paging, TCP handshake, database transaction timeline.
- Debugging demo: failing case, print trace, fixed version, tests.

## Output Pattern

1. Explain the concept in one paragraph.
2. Provide small runnable code.
3. Show expected output or state trace.
4. Explain what each step reveals.
5. Add one practice modification.

## Language Constraints

C++ beginner default:

- Use `iostream`, arrays/vector, functions, loops, conditionals.
- Avoid templates beyond standard containers, lambdas, smart pointers, advanced STL algorithms, operator overloading, and metaprogramming unless requested.

Python beginner default:

- Use lists, dictionaries, loops, functions.
- Avoid decorators, generators, advanced NumPy/Pandas unless relevant and known.

Java beginner default:

- Use classes only as needed, arrays/ArrayList, loops, methods.
- Avoid streams, generics-heavy abstractions, reflection, concurrency unless known.

Other languages (Rust, Go, MATLAB, R, etc.):

- Default to the simplest, most readable subset of the language.
- Avoid advanced features (e.g., in Rust: lifetimes, macros, unsafe; in Go: channels, interfaces with nil semantics, reflection; in MATLAB: object-oriented features, Simulink) unless the user has learned them or asks for them.
- If the language is uncommon for the course, ask the user for their learned scope before using advanced idioms.
- When the language has a REPL or notebook (MATLAB, R, Julia), prefer interactive-style demos over compiled-style boilerplate.

## Animation Choices

- Mermaid for static process flow.
- HTML Canvas or p5.js for browser animations.
- Manim for math/physics animations.
- Three.js for 3D concepts only when 3D materially helps.

For generated local demos, keep them as single-file artifacts when possible.

## Environment-Aware Demo Form

- **Agent shell**: write a single-file script in the appropriate language, run it, capture output, and show the result. Default to `.py` for concept demos and basic C++ for C++ course review. Save plots to a file the student can open.
- **RAG notebook**: emit a code block with the demo plus a separate fenced block with the expected output. If the notebook supports execution, the student can run it; if not, the expected output is the teaching artifact.
- **Notes app**: emit Markdown-native code blocks, expected output, and a trace table. Add tags such as `#程序设计` or backlinks such as `[[指针]]` only when helpful.
- **Plain chat**: same as RAG notebook — code block + expected output. Add one short walk-through of the key lines ("line 3 initializes the array, line 7 swaps…") so the student can read the code without executing it.

Never assume the student can run code in a plain chat. Always pair code with expected output or a trace table.
