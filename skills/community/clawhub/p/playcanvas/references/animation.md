# Animation

PlayCanvas provides a powerful state-based animation system which can be used to animate character models and other arbitrary scene object models. Users can work with any of their .FBX animation assets. These can be organized using animation state machines to easily control the animated behavior of scene models at runtime.
## System Overview
The animation system touches on three main areas of the PlayCanvas platform. This section will walk through how these areas can be used together to create complex animation behavior for your models. The following sections of the animation user manual then will explore each area in more detail.
### Animating in PlayCanvas
In order to begin animating a PlayCanvas entity, you must have a set of animation assets available and imported into your PlayCanvas project. These animation assets will drive the animation of a given model you wish to animate. For example a humanoid character may have a set of animations; Idle, Walk, Jump.
These three animations can be organized into a single animation system to create a simple locomotion system for that character. The way this is achieved in PlayCanvas is through the use of an animstategraph asset. These assets can be thought of as state machines for an entity's animation behavior. With each state in this asset relating to an animation, the state machine can be set up to define the complex animation behavior of an entity's model. This includes defining when the system should stop one animation and start another and how the transition between these animations should be blended.
The anim component is then used to assign an animstategraph asset to a particular entity in your scene. Once an entity has been assigned an animstategraph asset, each state in the graph can have an actual animation asset assigned to it. Once all states have been assigned animations, the anim component will become playable. At this point the animation system is complete and the defined animation behavior will be viewable in the PlayCanvas launcher.
### Anim Component
The anim component wires animstategraph assets and animation assets to entities. See [editor-scenes-components](editor-scenes-components.md) for details.
### Animation Assets
Animation assets are keyframe data that drives animations of a model in PlayCanvas. They are linked to an animstategraph asset via an entity's anim component. The anim component supports animation assets imported from .FBX files using the `Convert to GLB` asset task setting.
## Anim State Graph Assets
Animstategraph assets are used to organize a set of different animation states, which are all the various ways in which a model might animate. It can be used to define each of these animation states, determine when each state should play and how states transition and therefore blend between one another.  Actual animation assets are linked to the animstategraphs animation states through the [Anim Component](/user-manual/editor/scenes/components/anim/).
   
   
 An anim state graph can only be in one of these states at a given time.
 Animation states, along with the START state, END state and ANY state.  The other states are used to control the flow through the state machine.
### Animation States {#animation-states}
Animation states define a playable animation such as 'Idle', 'Jump' or 'Walk'. New animation states can be created by right clicking on the blank canvas behind the state graph and selecting 'Add new state' from the menu. The editor will target your newly created state and show its inspector panel on the right hand side. Within this inspector the following state variables can be modified:
| Variable | Description |
|----------|-------------|
| Name     | The name that this state should be called by. This is used to find and edit and play states via script. Names must be unique per state graph layer. |
| Speed    | The playback speed for animations that are linked to this state. |
| Loop     | Whether animations linked to this state should loop during playback. If set to false the animation will pause on its last keyframe until this state is exited. |
### START state {#start-state}
The START state is the entry point of every state graph. When an anim component begins playing its assigned anim state graph, it will first enter this state and transition directly to the animation state it's connected to. This animation state is called the default state and it can be selected via the layers panel here:
It is not possible to create any other transitions to or from the START state. It can only be entered again by transitioning to the END state.
### END state {#end-state}
The end state marks an exit out of the current state graph. If your animation state is set up to transition to the END state, the system will move directly to the default animation state which is connected to the START state. This is useful to create cyclical flows through the graph while still laying out your graph in a linear fashion. It is not possible to create transitions from the END state to any other state. It will always transition directly to the START state.
### ANY state {#any-state}
This state is used to create transitions which can be activated while the system is currently in any of the other animation states. Any transitions that trigger from this state will blend as if they had been connected directly from the currently active animation state. You can create transitions from the ANY state but not to it.
This is useful to set up transitions which you want to activate, no matter which state you're currently in. For example you could have a jump state which should be reachable from both an idle and walk state. Instead of setting up transitions from both the idle and walk states to the jump state, a transition can be set up between the ANY state and the jump state.
### Transitions {#transitions}
Transitions define how the anim state graph can move from one animation state to another. They can be created by right clicking an animation state and selecting `Add transition` from the context menu.
By setting the variables of a given transition you can also control how the animations of the transitioning states will blend together.
The available transition variables are:
| Variable            | Description |
|---------------------|-------------|
| Duration            | The duration of the transition in seconds. |
| Exit Time           | The time at which to exit the source state and enter the destination state. Given in normalized time based on the source state's duration. Providing no value allows the source state to exit with this transition at any time. A value of less than 1 will make the transition available for exit at that time during every loop of the source state. |
| Offset              | If provided, the destination state will begin playing its animation at this time. Given in normalized time based on the destination state's duration. Must be between 0 and 1. |
| Interruption Source | Defines whether another transition can interrupt this one and which of the current or previous states' transitions can do so. |
  
### Parameters {#parameters}
The parameters of an anim state graph are variables which are used to control the flow of animations during runtime. These variables can be accessed via scripts and set to new values at any time. They are then the way in which users can control the behavior of an entity's animation during its lifecycle.
New parameters can be added to a state graph via the parameters panel on the left inspector:
Each parameter has three variables which can be set:
| Variable      | Description |
|---------------|-------------|
| Name          | The name that this parameter should be called by. This is used to find and set the parameter via script. Names must be unique per state graph. |
| Type          | The type of variable that the parameter contains. One of: Boolean, Float, Integer or Trigger. The Trigger type acts as a Boolean but with the special property that its value is set back to false after it has been used to successfully activate a transition. |
| Default Value | The value of the parameters variable when the state graph launches. |
 Each transition in the graph can have a list of conditions which define when a transition is usable by the system. A state will not be able to pass to another state through a given transition unless all of its conditions are met.
 For example, the following condition:
Can be used in the transition between the Idle and Jump animation states to ensure that a character only jumps when the 'Jump' parameter has been set to true via a script.
### Layers {#layers}
  
     entity.anim.on('smile_start', (event) => {
      this.entity.anim.findAnimationLayer('smile').weight = 1;
    });
    this.entity.anim.on('smile_end', (event) => {
      this.entity.anim.findAnimationLayer('smile').weight = 0;
    });
  }
}
```
</TabItem>

</Tabs>
md), you can set the `blend type` of your layers to `Additive` to blend in an animation which only controls part of your model's bones. Updating the `blend weight` in real time as described above can allow you to create smooth blends between animations on different layers.  For example, you could have a `shooting` animation that is blended in and out on a characters upper body, while freeing up the lower body for various locomotion animations such as `walking` and `running`.
Any layers that are set to `Overwrite` will completely replace the animation values of the model's bones that are animated in that layer. 
## Anim Events
Anim events can be used to trigger event listeners during the playback of an animation. Each event is associated with a specified frame of the animation asset it is attached to. When the playback of the animation reaches that frame, the event will fire and the associated event listener is called.
### Creating Events
To create a new event, select the animation asset in the asset panel which you'd like to create an event for. You should then see the `+ EVENT` button in the asset inspector as shown below:
Each event has the following modifiable properties:
| Variable | Description |
|----------|-------------|
| time     | Defines the specific time during the playback of the animation when the event should trigger. Given in seconds. |
| name     | The name of the event is used to identify the event when attaching an event listener to the anim component. |
| number   | An additional property which can be set to any number. Used to pass additional details to the event listener. |
| string   | An additional property which can be set to any string. Used to pass additional details to the event listener. |
### Event Listeners
After creating an event for an animation asset, the event will be fired whenever that asset is played back by an anim component. You can therefore attach listeners to the anim component to handle the event. The following example shows how to attach event listeners to the anim component:

Any number of animation events can be attached to a single animation asset and used by any number of anim components. Making use of the additional `number` and `string` properties of an event allows you to differentiate between events that are passed to the same event listener.
## Anim Layer Masking
When creating complex animation behavior for your game objects, it is often necessary to isolate the playback of certain animations to specific bones in each object's model.  This can be achieved in PlayCanvas by creating a mask for a given [animation layer](/user-manual/animation/anim-state-graph-assets/#layers) in your anim component.
### Creating a mask
After creating an Anim State Graph asset and attaching it to an anim component, you'll be presented with a list of layers contained in your graph. You can create a mask for any of these layers by clicking the **Create Mask** button under each layer panel:
 This will open up the mask inspector for that layer which is shown below:
The mask inspector displays the full hierarchy which the anim component is driving, starting at the `root bone` specified in the anim component. Each bone in the hierarchy can be selected to be included in the mask. You can also right-click specific bones to include or exclude whole sections of the hierarchy. Any bones which are not selected in this mask will not be driven by any of the animations which play in this mask's layer.
After creating masks, you can use [layer blending](/user-manual/animation/anim-state-graph-assets/#layer-blending) to smoothly blend the masked animations of multiple layers together.
