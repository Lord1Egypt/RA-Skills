# ClawHub Listing Draft

## Name

One Person Company OS

## Short Description

Build a visual operating cockpit for an AI-native one-person company

## Primary Pitch

One Person Company OS turns an AI product idea into a visible business loop:

- promise
- buyer
- product capability
- delivery
- cash
- learning
- asset

The founder gets an **Operating Cockpit** as the first reading surface. It shows the current bottleneck, revenue pipeline, business-loop map, shortest action, and links into the editable workspace.

## What Users Get

- localized operating cockpit HTML
- editable markdown work surfaces
- numbered DOCX formal deliverables
- deterministic SVG visuals for the business loop and revenue pipeline
- optional AI image prompts for covers, launch posts, and promotional visuals
- role briefs, reminders, flow notes, and starter deliverables aligned to the same operating loop
- runtime transparency and Python compatibility guidance

## First-Run Promise

The first serious run should produce:

- a clear sellable promise
- the first buyer definition
- the primary bottleneck
- the primary arena to push next
- the operating cockpit
- a workspace surface that matches the founder language
- deterministic visual assets
- optional AI image prompts for promotion
- the shortest action for today
- a local hidden machine-state file under the approved workspace

## Quick Start Prompts

- `clawhub install one-person-company-os`
- `I am building a one-person AI company. Use one-person-company-os v1.0. First help me confirm the sellable promise, first buyer, and core problem. Then create the approved local workspace, open with the operating cockpit, show the current bottleneck visually, and save only approved files inside that workspace.`
- `我正在创建一个 AI 一人公司，请调用 one-person-company-os v1.0。先帮我确认可卖承诺、第一批买家和核心问题；确认后在我批准的本地目录创建工作区，用经营驾驶舱作为入口，直观展示当前瓶颈，并且只把批准后的文件保存到这个工作区内。`

## Safety Boundary

- script mode expects an existing local `Python 3.7+`
- `scripts/ensure_python_runtime.py` prints compatibility and manual install guidance only
- the marketplace build does not auto-install system packages
- persisted files stay inside the approved workspace
- normal use does not require API keys or unrelated credentials
- AI image generation is optional and not part of the required runtime path

## Trust Boundary

The founder is still the decision-maker.
The system can draft, update, persist, visualize, and tighten the loop, but pricing changes, budget spend, launch claims, legal statements, high-risk customer actions, and writes outside the approved workspace still require explicit founder approval.
