# PlayCanvas React

## React
[@playcanvas/react](https://github.com/playcanvas/react) brings PlayCanvas to the React ecosystem. It provides a declarative, component-based approach to building interactive 3D applications using familiar React patterns and a powerful ECS architecture.
PlayCanvas has a powerful ECS architecture that aligns perfectly with React's declarative nature. You create Entities, add Components to them, and load assets.
## Quick Example
```jsx
export const Lambo = () => {
  const { asset: model } = useModel('/assets/lambo.glb');
  if (!model) return null;
  return <>
    <Entity name='camera' position={[4, 1, 4]}>
      <Camera clearColor='#090707' fov={28} />
      <OrbitControls zoomRange={[3, 6]} pitchRange={[-90, -5]}/>
    </Entity>
    <Render type='asset' asset={model}/>
  </>
}
```
## Getting Started
```bash
npm create playcanvas@latest -- -t react-ts
```
This creates a new project with everything set up. You can also try the [online playground](https://playcanvas-react.vercel.app/new) to experiment without installing anything locally.
PlayCanvas React gives you access to the entire PlayCanvas Engine — no third-party libraries required. It adds React-first features to make development faster and more ergonomic.
## Recommended: Scaffold a New Project
```bash
npm create playcanvas@latest -- -t react-ts
```
This creates a new project with everything set up. Follow the prompts and you'll have a PlayCanvas React project running in your browser.
## Add to Existing Project
```bash
npm install @playcanvas/react
```
Use your preferred package manager. Once installed, follow the [building a scene guide](/user-manual/react/building-a-scene/) to create your first project.
## Building A Scene
## Your First Scene
```jsx
import { Application, Entity } from '@playcanvas/react';
import { Render, Camera } from '@playcanvas/react/components';
const Scene = () => (
  <>
    <Entity name='box'>
      <Render type='box'/>
    </Entity>
  </>
);
export const App = () => (
  <Application>
    <Entity name='camera' position={[0, 0, 5]}>
      <Camera />
    </Entity>
    <Scene />
  </Application>
);
```
PlayCanvas uses an ECS architecture — you add components to an Entity to give it functionality. The `Application` is the root, setting up a canvas and rendering context.
## Adding Lights
Add environmental lighting with `useEnvAtlas` and the `Environment` component, plus a directional light:
```jsx
const { asset: envAtlas } = useEnvAtlas('/assets/environment.png');
<Environment envAtlas={envAtlas} />
<Entity name='directional-light' position={[0, 0.001, 0]}>
  <Light type='directional' />
</Entity>
```
## Adding Interactivity with Scripts
Use `Script` components for performant, frame-based interactivity outside the React render loop:
```jsx
<Entity name='camera' position={[4, 1, 4]}>
  <Camera clearColor='#090707' fov={28} renderSceneColorMap={true} />
  <Script script={CameraControls} enableFly={false}/>
</Entity>
```
## Adding 3D Models
Load models with hooks and render with the `Render` component:
```jsx
const { asset: lambo } = useModel('/assets/lambo.glb');
if (!lambo) return null;
<Entity name='model'>
  <Render type='asset' asset={lambo} />
</Entity>
```
## Staging with Ground and Shadows
```jsx
<ShadowCatcher width={5} depth={5} />
<Entity name='grid' scale={[1000, 1, 1000]}>
  <Script script={GridScript}/>
</Entity>
```