# Real-time Collaboration

Real-time collaboration is at the heart of the PlayCanvas Editor. This brings a number of benefits:
* 🧑‍🤝‍🧑 Multiple users can work together to build a scene.
* 🆘 One user can join another to offer advice or help fix an issue.
* 🔍 Stakeholders can drop by to see the latest state of a project.
Let's examine how real-time collaboration is surfaced in the interface.
## Presence Bar
In the bottom left corner of the [Viewport](../interface/viewport) (next to the CHAT button), you will find the Presence Bar.
Whenever a new user enters the scene, their user avatar will be added to the Presence Bar. Likewise, when they close the Editor, their avatar will be removed from the Presence Bar. You can hover any avatar to view the associated username. And if you click an avatar, it will take you to that user's profile page.
## Real-time Chat {#real-time-chat}
If you select the CHAT button, the Chat panel will expand and you can broadcast messages to other users present in the Editor with you.
You can toggle browser notifications for chat messages in the [Settings](interface/settings/editor.md#settings).
## Viewport Cameras
Each user in the scene is represented in the [Viewport](../interface/viewport) by a colored, wireframe camera frustum.
Mouse over the shaded center plane of a user camera to view the associated username:
## Selection Indicators
It can be useful to know what entities other users are selecting and potentially editing. The [Hierarchy](../interface/hierarchy) displays square indicators to the right of entities selected by other users (shaded according to their user color).
Whenever an entity with a 3D model is selected by any user, its outline will be rendered in the [Viewport](../interface/viewport).
