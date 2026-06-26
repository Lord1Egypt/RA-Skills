# Gaussian Splatting

## Splatting Index
3D Gaussian Splatting is a revolutionary technique for capturing, representing, and rendering photorealistic 3D scenes. Unlike traditional polygonal meshes, Gaussian Splatting uses millions of small, semi-transparent elliptical splats to reconstruct detailed environments with exceptional visual fidelity.
## What Makes Gaussian Splatting Special?
Gaussian Splatting excels at capturing real-world environments through photogrammetry, making it incredibly quick and affordable to generate high-quality 3D content. The technique is particularly powerful for:
- **Photorealistic environments** - Capture real locations with stunning visual detail
- **Rapid content creation** - Generate complex 3D scenes from simple photo/video capture
- **Volumetric representation** - Handle translucent materials, fine details, and complex lighting naturally
- **Real-time rendering** - Optimized for interactive frame rates in web browsers
## PlayCanvas Gaussian Splatting Workflow
PlayCanvas provides a complete ecosystem for working with Gaussian Splats:
1. **[Creating Splats](creating)** - Methods for creating your own splat data
2. **[Viewing Splats](viewing)** - Preview and evaluate splats using the PlayCanvas Model Viewer
3. **[Editing Splats](editing)** - Clean up and prepare splats for optimal rendering
4. **[Building Splat-based Apps](building)** - Integrate splats into your PlayCanvas projects
## Splatting Viewing
Once you've created a Gaussian splat, you'll want to preview and evaluate it before proceeding to editing or integration into your projects. The **PlayCanvas Model Viewer** provides a convenient way to quickly view and inspect your splat files without needing to set up a full PlayCanvas project.
## PlayCanvas Model Viewer
The [PlayCanvas Model Viewer](https://playcanvas.com/viewer) is a web-based tool that allows you to instantly preview 3D content, including Gaussian splats, directly in your browser.
<video autoPlay muted loop controls src='/video/playcanvas-splat-viewer.mp4' style={{width: '100%', height: 'auto'}} />
### Supported Splat Formats
The Model Viewer supports the following commonly used Gaussian splat formats:
| Format | File Extension | Description |
|--------|----------------|-------------|
| **PLY** | `.ply` | Standard uncompressed splat format |
| **Compressed PLY** | `.compressed.ply` | Compressed (quantized) format |
| **SOG (bundled)** | `.sog` | Super-compressed format in single file |
| **SOG (unbundled)** | `meta.json` + `.webp` images | Super-compressed format in multiple files |
### How to View Your Splats
1. **Visit** [playcanvas.com/viewer](https://playcanvas.com/viewer)
2. **Drag and drop** your splat from your file system onto the viewer
3. **Navigate** the 3D scene:
   | Control | Action |
   |---------|--------|
   | Left double click | Set orbit point |
   | Left click + drag | Orbit around the splat |
   | Right click + drag | Look around |
   | Shift + click + drag | Pan the view |
   | Mouse wheel | Zoom in/out |
   | WASD or Arrow keys | Move forwards/backwards/left/right |
## Open Source and Customization
The PlayCanvas Model Viewer is **open source** and available on [GitHub](https://github.com/playcanvas/model-viewer). This means you can:
- **Host your own version** - Use a local server or deploy to your own infrastructure for complete control
- **Add new functionality** - Add support for additional file formats or custom UI
- **Contribute back** - Submit issues and pull requests to help improve the viewer for everyone