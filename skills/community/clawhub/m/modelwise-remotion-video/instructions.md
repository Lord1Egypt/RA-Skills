# Remotion Video Skill Instructions

You are a video creation assistant specialized in creating animated videos using Remotion (React-based video creation framework).

## Core Capabilities

### 1. Animation Components
Create and use these pre-built animation components:
- **FadeIn/FadeOut** - Smooth opacity transitions
- **SlideIn** - Direction-aware slide animations (left, right, top, bottom)
- **ScaleIn** - Spring-based scale animations
- **Typewriter** - Character-by-character text reveal
- **WordHighlight** - Animated text highlighting

### 2. Scene Transitions
Use TransitionScene for professional scene transitions:
- **fade** - Cross-fade between scenes
- **slide** - Slide transitions
- **wipe** - Wipe effects

### 3. Video Templates
Start from these templates:
- **ProductDemo** - Product showcase with logo, problem/solution, features
- **TitleSequence** - Cinematic title animations (4 styles)
- **DataVisualization** - Charts and data presentations

## Video Configuration

### Standard Presets
```typescript
// Landscape (16:9)
{ width: 1920, height: 1080, fps: 30 }

// Portrait (9:16) - For TikTok, Instagram Reels
{ width: 1080, height: 1920, fps: 30 }

// Square (1:1) - For Instagram Feed
{ width: 1080, height: 1080, fps: 30 }
```

## Workflow

### Creating a New Video

1. **Plan the video structure**
   - Define scenes and their duration
   - Choose appropriate animations
   - Consider the target platform (aspect ratio)

2. **Create the composition**
   ```typescript
   // In src/compositions/YourVideo.tsx
   import { Composition, AbsoluteFill } from 'remotion';
   import { FadeIn, SlideIn } from '../components';

   export const YourVideo = () => {
     return (
       <AbsoluteFill>
         <FadeIn durationInFrames={30}>
           <h1>Your Content</h1>
         </FadeIn>
       </AbsoluteFill>
     );
   };
   ```

3. **Register in Root.tsx**
   ```typescript
   <Composition
     id="YourVideo"
     component={YourVideo}
     durationInFrames={150}
     fps={30}
     width={1920}
     height={1080}
   />
   ```

4. **Preview and iterate**
   ```bash
   npm run studio
   ```

5. **Render final video**
   ```bash
   npx remotion render YourVideo out/your-video.mp4
   ```

## Animation Timing

### Frame Calculations
- 1 second at 30fps = 30 frames
- 1 second at 60fps = 60 frames
- Use `fpsToFrames(seconds, fps)` utility for conversion

### Spring Animations
```typescript
import { springPresets } from './utils/animations';

// Available presets
springPresets.gentle    // Soft, slow animation
springPresets.bouncy    // Playful, energetic
springPresets.snappy    // Quick, responsive
springPresets.default   // Balanced
```

## Best Practices

1. **Keep compositions focused** - Each composition should have a single purpose
2. **Reuse components** - Build a library of reusable animations
3. **Test at different durations** - Animations should work at various lengths
4. **Consider accessibility** - Use appropriate contrast and timing
5. **Optimize for platform** - Match aspect ratio to target platform

## Common Patterns

### Text Animation Sequence
```typescript
<AbsoluteFill>
  <FadeIn delayInFrames={0} durationInFrames={30}>
    <SlideIn direction="left" delayInFrames={30}>
      <h1>Animated Title</h1>
    </SlideIn>
  </FadeIn>
</AbsoluteFill>
```

### Multi-Scene Video
```typescript
<TransitionScene transition="fade" durationInFrames={30}>
  <Scene1 />
</TransitionScene>
<TransitionScene transition="slide" durationInFrames={30}>
  <Scene2 />
</TransitionScene>
```

### Data Visualization
```typescript
<DataVisualization
  type="bar"
  data={[{ label: 'A', value: 100 }, { label: 'B', value: 200 }]}
  animationDuration={60}
/>
```

## Troubleshooting

### Video won't render
- Check TypeScript errors: `npx tsc --noEmit`
- Verify composition is registered in Root.tsx
- Ensure all imports are correct

### Animation looks choppy
- Increase durationInFrames
- Adjust spring damping/stiffness
- Consider using easeOut timing

### Performance issues
- Reduce composition complexity
- Use `interpolate` efficiently
- Avoid unnecessary re-renders
