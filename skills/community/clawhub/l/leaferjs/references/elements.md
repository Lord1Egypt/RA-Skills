# Graphic Elements

## Shapes

```ts
Rect:     new Rect({ width:100, height:100, cornerRadius:[0,40,20,40], fill:'#32cd79' })
Ellipse:  new Ellipse({ width:100, height:100, startAngle:-60, endAngle:180, innerRadius:0.5 })
Line:     new Line({ width:100, strokeWidth:5, stroke:'#32cd79' })
Polygon:  new Polygon({ width:100, height:100, sides:6, cornerRadius:10 })
Star:     new Star({ width:100, height:100, innerRadius:0.5, corners:8 })
Path:     new Path({ path:'M10 10 L100 100', fill:'#32cd79' })
Pen:      pen.setStyle({fill:'red'}).roundRect(0,0,100,100,30).arc(50,50,25)  // Canvas 2D API
Image:    new Image({ url:'/image.jpg', draggable:true })
Text:     new Text({ fill:'#32cd79', text:'Hello' })
Canvas:   new Canvas({ width:200, height:200 })  // .context → CanvasRenderingContext2D
```

## Styles

```ts
fill:       '#32cd79' | { type:'linear', stops:['red','blue'] } | { type:'image', url:'...' }
stroke:     { stroke:'red', strokeWidth:2, strokeAlign:'center', strokeCap:'round', strokeJoin:'miter', dashPattern:[6,6] }
shadow:     { x:10, y:-10, blur:20, color:'#FF0000AA' }
innerShadow:{ x:10, y:5, blur:20, color:'#FF0000AA' }
mask:       true  // Mask (5 types)
eraser:     true  // Erase (2 types)
opacity:    0.5
blendMode:  'multiply'
origin:     'center'       // CSS transform-origin
around:     'center'       // Anchor (similar to game engine anchor)
visible:    false          // Hide
```

Modify: `rect.fill='blue'` / `rect.set({fill:'blue'})` / `rect.reset()` / `rect.reset({fill:'red'})`

## Coordinates & Bounding Box

5 coordinate systems: world(canvas) → page(within tree) → local(relative to parent) → inner(within element) → box(content top-left)

```ts
element.getPagePoint(pt)      // world→page
element.getInnerPoint(pt)     // world→inner
element.getBoxPoint(pt)       // world→box
app.getWorldPointByClient(e)  // client→world
element.boxBounds             // OBB basic bounds
element.worldBoxBounds        // AABB world-space box
element.getLayoutBounds()     // OBB (including rotation/scale)
new Bounds(r1.boxBounds).hit(r2.worldBoxBounds)  // Collision detection
```

## Export (requires @leafer-in/export)

```ts
rect.export('test.png')                                  // Download
rect.export('HD.png', { pixelRatio: 2 })                 // HD
rect.export('jpg').then(r => console.log(r.data))        // Base64
rect.export('png', { blob: true })                       // Binary
leafer.export('screenshot.png', { screenshot: true })    // Screen capture
leafer.toJSON()                                          // → JSON
```

## Remove, Destroy & Performance

```ts
rect.remove()                  // Remove
rect.destroy()                 // Remove + destroy
leafer.remove('#book')         // Conditional remove
leafer.clear()                 // Clear all
leafer.destroy(true)           // Destroy engine (sync)
leafer.forceRender()           // Force re-render
leafer.start()/stop()          // Start/stop
```

**Performance (million-rectangle benchmark):** Creation 1.28s / 320MB RAM / 60FPS dragging (traditional libraries ~9-15s / 2-4GB)

**Partial rendering:** `usePartRender:true` (default) only updates changed areas. Disable with: `{ usePartRender:false }`

## Animation (requires @leafer-in/animate)

```ts
// animation (enter)
new Rect({ animation: { style:{ x:500 }, duration:1, swing:true } })
// animationOut (exit)
new Rect({ animationOut: { style:{ opacity:0 }, duration:0.8 } })
// Keyframes
new Rect({ animation: { keyframes:[{ style:{ x:150 }, duration:0.5 }, { x:50, rotation:-720 }], duration:3, loop:true }})
// transition
new Rect({ transition: { duration:0.5, easing:'ease' } })
```