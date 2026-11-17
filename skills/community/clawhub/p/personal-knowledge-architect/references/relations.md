# Eight Relation Types

Read this while building the round-two relation graph. Every edge must support later assembly; keep
two to six per concept. If one element still works without the other, use reference rather than
dependency.

| Type          | Direction                            | Use when                                                                                |
| ------------- | ------------------------------------ | --------------------------------------------------------------------------------------- |
| contains      | concept → concept or entity → entity | whole and part                                                                          |
| depends-on    | concept → concept                    | execution is impossible without the target                                              |
| references    | concept → concept                    | mentioned but independently usable                                                      |
| invokes       | scene/concept → concept/entity       | used during assembly or execution                                                       |
| decomposes-to | concept → sub-concept                | stages of a procedural concept                                                          |
| parent-child  | entity → entity                      | hierarchy of at most three levels; child has its own source, definition, and references |
| assembles     | scene stage → concept/entity         | stage orchestration rule                                                                |
| alias         | knowledge element → name             | naming variant, not another element                                                     |

Decide in order: can it execute without the target (dependency vs reference)? Is the target a part
or a stage (contains vs decomposes)? Who uses it (invokes vs assembles)? Keep only the strongest
relation for a pair.
