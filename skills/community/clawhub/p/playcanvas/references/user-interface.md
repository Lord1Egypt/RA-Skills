# User Interface

## Interface
User Interfaces present a unique challenge for graphical applications. There are several options for building User Interfaces in PlayCanvas.
## Screen and Element Components (Recommended)
PlayCanvas implements two components which can form the building blocks of a user interface system that runs directly inside your WebGL canvas. The **Screen Component** is the user interface container, and the **Element Component** is used to add user interface elements. The primary advantage is that your user interface exists in the same context as the rest of your game. This allows interactions between the application and the user interface.
## HTML and CSS
Web browsers have spent years building effective and optimized systems for rendering complex interfaces to users. For some use cases using the HTML, CSS and the browser DOM are a good fit for your user interface.
The primary downside of using the DOM is performance. The DOM is not designed to be run in a high framerate, real time setting. Page reflows and garbage collection can cause stutters in your application. If you're aiming for a consistent 60fps in your application this is not the best option.
---
The rest of this user guide will focus on the Screen and Element component system and using them to build user interfaces in PlayCanvas.
## Interface Screen
The Screen Component defines the area and rendering of a user interface. Children added to a Screen Component should all have an Element Component.
## Properties
| Property | Description |
|----------|-------------|
| Screen Space | When enabled, renders in 2D as overlay to the canvas |
| Resolution | (3D mode) Screen coordinate resolution (width × height). Coordinates increase right and up. |
| Ref Resolution | (Screen Space, Blend mode) Reference resolution for calculating scale factor |
| Scale Mode | (Screen Space) None (no scaling) or Blend (scales by ratio of reference to actual resolution) |
| Scale Blend | (Screen Space, Blend) Weighting between horizontal (0) and vertical (1) scaling |
| Priority | Render order (0-127). Higher = rendered on top. |
## Usage
1. Create an Entity with a Screen Component
2. Set Screen Space on/off depending on 2D overlay vs 3D UI
3. Configure resolution and scaling
4. Add child entities with Element Components for UI content
5. Add Button Components for interactive elements