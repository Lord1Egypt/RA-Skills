---
name: opentui
description: OpenTUI — Zig-native terminal UI framework. Covers installation, renderer, components (Text/Box/Input/Select/Code/ScrollBox), Constructs declarative API, Flexbox layout, React/Solid bindings. 
---

# OpenTUI — Native Terminal UI Framework

Zig-native TUI core with TypeScript bindings and Yoga Flexbox layout. Powers OpenCode in production.

## Use Cases

Use when building terminal TUI applications.

## Installation

```bash
bun init -y && bun add @opentui/core
# React: bun add @opentui/react @opentui/core react; bun create tui --template react
# Solid: bun add solid-js @opentui/solid
```

## Renderer

```typescript
const r = await createCliRenderer({
  screenMode: "alternate-screen"|"main-screen"|"split-footer",
  targetFps: 30, exitOnCtrlC: true, useMouse: true, autoFocus: true,
  backgroundColor: "transparent", consoleMode: "console-overlay"|"disabled",
})
r.root.add(Text({ content:"Hello", fg:"#0F0" }))
r.start()/stop()/pause()/suspend()/resume()/destroy()
r.on("resize",(w,h)=>{}); r.on("focus"|"blur"|"destroy",()=>{})
r.on("theme_mode",m=>{}); r.on("selection",s=>s.getSelectedText())
r.setTerminalTitle("t"); r.setBackgroundColor("#0D1117")

// Scrollback (split-footer mode)
r.writeToScrollback(ctx=>({root,width:ctx.width,height:1,startOnNewLine:true}))
const sf = r.createScrollbackSurface({}); sf.root.add(code); sf.settle(); sf.destroy()
```

## Components

```typescript
// Text
Text({content:"hello",fg:"#F00",bg:"#222",attributes:BOLD|UNDERLINE,selectable:true,position:"absolute",left:10,top:5})
// Attributes: BOLD DIM ITALIC UNDERLINE BLINK INVERSE HIDDEN STRIKETHROUGH
// Inline template: t`${bold("t")}: ${fg("#F00")(italic("w"))} normal`

// Box
Box({width:30,height:10,borderStyle:"rounded"|"single"|"double"|"heavy",borderColor:"#FFF",
     title:"Settings",titleAlignment:"left"|"center"|"right",padding:1,gap:1,
     onMouseDown:()=>{},onMouseOver:()=>{},onMouseOut:()=>{}})

// Input
Input({width:25,placeholder:"Type...",backgroundColor:"#222",focusedBackgroundColor:"#333",
       textColor:"#FFF",cursorColor:"#0F0"})
input.focus(); input.value="new"; // Events: INPUT / CHANGE / ENTER

// Select
Select({width:30,height:8,options:[{name:"Option",description:"desc",value:any}],
        selectedIndex:0,backgroundColor:"#1a1a1a",selectedBackgroundColor:"#333366"})
// Arrow keys/jk navigate, Enter to select; Events: ITEM_SELECTED / SELECTION_CHANGED

// Code (Tree-sitter)
const style = SyntaxStyle.fromStyles({keyword:{fg:RGBA.fromHex("#FF7B72"),bold:true},default:{fg:RGBA.fromHex("#E6EDF3")}})
Code({content:"const x=1",filetype:"typescript",syntaxStyle:style,streaming:false,width:50,height:10})
// Markdown: MarkdownRenderable({content:"# H1",syntaxStyle,streaming:true,conceal:true})
// Diff: DiffRenderable({view:"unified"|"split",syncScroll:true,diff:"patch",syntaxStyle})

// ScrollBox
ScrollBox({width:40,height:20,scrollY:true,stickyScroll:true,stickyStart:"bottom"|"top",
           viewportCulling:true,scrollbarOptions:{showArrows:true,trackOptions:{foregroundColor:"#7aa2f7"}}})
// Keyboard: ↑↓/pgup/pgdn/home/end; Methods: scrollBy(y)/scrollTo({x,y})/scrollChildIntoView("id")
```

Others: `TextArea` `TabSelect` `ASCIIFont({text:"T",font:"tiny"})` `LineNumberRenderable({target:code})`

## Constructs (Declarative API)

```typescript
Box({width:40,borderStyle:"rounded",padding:1}, Text({content:"Hi"}), Input({placeholder:"..."}))
// VNodes queue method calls: input.focus() → auto-executed when added to tree

function LabeledInput({id,label,pl}) {
  return delegate({focus:`${id}-in`},
    Box({flexDirection:"row"}, Text({content:label}),
    Input({id:`${id}-in`,placeholder:pl,width:20})))
}
// delegate({focus:"child-id"}, vnode) routes methods to child components

function Card({title},...children) {
  return Box({border:true,padding:1,flexDirection:"column"},
    Text({content:title,fg:"#FF0"}), Box({flexDirection:"column"},...children))
}
```

## Flexbox Layout (Yoga)

```typescript
Box({flexDirection:"row"|"column"|"row-reverse"|"column-reverse",
     justifyContent:"center"|"space-between"|"space-around"|"space-evenly",
     alignItems:"center"|"stretch"|"baseline",
     flexGrow:1,flexShrink:0,flexBasis:100,
     width:"100%"|30,height:"50%"|10,
     position:"absolute",left:10,top:5,right:10,bottom:5,
     padding:2,paddingX:4,paddingTop:1,margin:1,gap:1})
// Responsive resize: r.on("resize",(w,h)=>{w<80&&(container.flexDirection="column")})
```

## React Bindings

```typescript
// tsconfig: "jsx":"react-jsx","jsxImportSource":"@opentui/react"
import {createRoot} from "@opentui/react"
createRoot(await createCliRenderer()).render(<App />)
// JSX: <text> <box> <scrollbox> <input> <textarea> <select> <code> <diff> <markdown>
// Style modifiers: <bold> <italic> <underline> <inline> <br/> <link>
// Hooks: useRenderer() useKeyboard((k)=>{}) useOnResize((w,h)=>{})
//        useTerminalDimensions() usePaste((e)=>{}) useFocus/useBlur(()=>{})
//        useSelectionHandler((sel)=>{}) useTimeline({duration,loop})
```

## Solid Bindings

```typescript
// tsconfig: "jsx":"preserve","jsxImportSource":"@opentui/solid"
// bunfig.toml: preload=["@opentui/solid/preload"]
import {render} from "@opentui/solid"
render(()=><App />) // snake_case component names: ascii_font tab_select
// Hooks same as React + Portal(<Portal mount={r.root}>), Dynamic(<Dynamic component="textarea"/>)
// Build: import solidPlugin from "@opentui/solid/bun-plugin"; Bun.build({plugins:[solidPlugin]})
```