# Examples

Minimal examples for common diagram types and directions.

## Sequence Diagram

```typescript
renderMermaidAscii(`
sequenceDiagram
  Alice->>Bob: Hello
  Bob-->>Alice: Hi
`)
```

## Class Diagram

```typescript
renderMermaidAscii(`
classDiagram
  Animal <|-- Duck
  Animal: +int age
  Duck: +swim()
`)
```

## ER Diagram

```typescript
renderMermaidAscii(`
erDiagram
  CUSTOMER ||--o{ ORDER : places
`)
```

## Flowchart Directions

```typescript
renderMermaidAscii(`graph TD\n  A --> B`)
renderMermaidAscii(`graph LR\n  A --> B`)
renderMermaidAscii(`graph BT\n  A --> B`)
```
