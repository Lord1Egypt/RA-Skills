# PlayCanvas Engine

It is possible to build applications on the PlayCanvas Engine without using the Editor. Some examples of applications built directly against the Engine are:
* [glTF Viewer](https://playcanvas.com/viewer) \[[GitHub](https://github.com/playcanvas/model-viewer)\]
* [SuperSplat](https://playcanvas.com/supersplat/editor) \[[GitHub](https://github.com/playcanvas/supersplat)\]
* ...and, of course, the [PlayCanvas Editor](../../editor) itself!
This page guides you in how to get started.
When setting up your project, there are two main options to consider.
## Option 1: Build Tool and NPM
This is the recommended set up that should suit most developers.
A build tool can bundle your application into an optimized package that can run on a wide range of browsers. There are many build tools such as [webpack](https://webpack.js.org/), [Rollup](https://rollupjs.org/) and [esbuild](https://esbuild.github.io/), and PlayCanvas will work with all of them. Here, we will use [Vite](https://vitejs.dev/), a popular build tool that aims to provide a faster and leaner development experience for modern web projects.
First, select whether you prefer to develop in JavaScript or TypeScript:

