---
name: plantuml-render
description: Render PlantUML diagrams using the PlantUML JAR. Use this skill to generate PNG/SVG/PDF images from PlantUML source code.
---

## How It Works

1. use write tool save plantUML file that include user need info (tips class digram not use extends or implements)
2. run python script to rander to image
3. The skill runs the PlantUML JAR (`plantuml.jar` in the same directory) via `java -jar`.

### Example
```shell
python /Users/jiafei/openclaw/skills/plantuml-render/scripts/plantuml.py {file_name.puml}
```

the image can be linke with markdown 

![as](example.png)