# PCUI

PCUI stands for **P**lay**C**anvas **U**ser **I**nterface. It is the front-end framework on which all PlayCanvas tools are built:
* [PlayCanvas Editor](https://github.com/playcanvas/editor)
* [SuperSplat](https://superspl.at/editor)
* [Model Viewer](https://playcanvas.com/viewer)
* [Texture Tool](https://playcanvas.com/texture-tool)
PCUI is open source and available on [GitHub](https://github.com/playcanvas/pcui). As such, you can use it in your own projects. This guide shows you how!
## Getting Started
Before you begin, make sure you have [Node.js](https://nodejs.org/) 18 or later installed.
## Installing from NPM
PCUI is available as a package on [NPM](https://www.npmjs.com/package/@playcanvas/pcui). You can install it as follows:
```bash
npm install @playcanvas/pcui --save-dev
```
This will include the entire PCUI library in your project. The various parts of the library will be available to import from that package at the following locations:
- Observers: `@playcanvas/observer`
- ES Module Components: `@playcanvas/pcui`
- React Components: `@playcanvas/pcui/react`
You can import the ES Module components into your own `.js` files and use them as follows:
```javascript
import { Button } from '@playcanvas/pcui';
import '@playcanvas/pcui/styles';
const button = new Button({
    text: 'Click Me'
});
document.body.appendChild(button.dom);
```
This will result in your first component being appended to your document body!
<div className='iframe-container'>
</div>
## API Reference
The [API reference](https://api.playcanvas.com/pcui/) is a list of all of PCUI's class components and their properties. It is automatically generated from the source code.
## React
PCUI components can be used directly in React applications. Import the components from the React package and use them in your `.jsx` files as follows:
```jsx
import * as React from 'react';
import ReactDOM from 'react-dom';
import { TextInput } from '@playcanvas/pcui/react';
import '@playcanvas/pcui/styles';
ReactDOM.render(
    <TextInput />,
    document.body
);
```
This example renders a basic text input component. You can see it in action below:
<div className='iframe-container'>
</div>
For more complex implementations, check out the [examples](../examples) section.
## Storybook
The [PCUI Storybook](https://playcanvas.github.io/pcui/storybook/) provides an interactive showcase of all available components. You can:
- Explore each component's properties and behavior
- Test different configurations in real-time
- View component documentation
- Copy example code
