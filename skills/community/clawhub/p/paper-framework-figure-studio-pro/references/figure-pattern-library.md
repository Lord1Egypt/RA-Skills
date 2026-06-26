# Framework Figure Pattern Library

Use these layout patterns after the reader effect and primary subtype are known.

## Layout Patterns

| Pattern | Use When | Strength | Risk |
|---|---|---|---|
| Left-to-right pipeline | The method is staged and sequential | Fast 10-second comprehension | Can hide feedback loops |
| Layered architecture stack | Components have abstraction levels | Clear module boundaries | Can feel generic |
| Hub-and-spoke model center | One core module coordinates inputs/tools/memory | Highlights novelty | Can over-center one block |
| Swimlane system diagram | Data/user/tool/model roles must be separated | Good for agent/system papers | Needs strong label discipline |
| Loop / agent workflow | Planning, tool use, verification, or memory updates repeat | Shows dynamics | Arrows can become cluttered |
| Modular tile board | Many modules or evidence cards need comparison | Scannable, modern | Weak sequence unless arrows are clear |
| Mechanism snapshot | One mechanism explains why the method works | Strong for intro/method bridge | May omit operational details |
| Case walkthrough strip | A concrete example travels through the method | Intuitive for qualitative papers | Not enough for full method spec |
| Baseline-vs-ours split | Novelty is comparative | Reviewer-friendly contrast | Can become adversarial or oversimplified |

## Framework-Specific Prompt Rules

- Give every module a short, exact label.
- Make novelty visually salient without turning every box into a highlight.
- Use arrows with semantics: data flow, control flow, feedback, supervision, or evidence link.
- Keep secondary details in caption/body text unless they are needed for the 10-second reader effect.
- When multiple layout patterns are plausible, present 4-6 text candidates and recommend a 6-image schematic board.

## Anti-Patterns

- Generic boxes with no novelty hierarchy.
- Too many equal-weight arrows.
- Text paragraphs inside the figure.
- Fake plots or invented numeric results.
- Decorative icons that do not carry method meaning.
- Photorealistic clutter for reviewer-sensitive method figures.
