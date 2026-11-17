# Vehicle Scene Ledger Example

Use this ledger with `--strict-continuity` for scenes inside cars, vans, trains, taxis, elevators, booths, or other narrow spaces.

## Fixed Facts

- Vehicle: four-door sedan, left-hand drive.
- Weather: raining lightly; windows fog at the edges.
- The car is moving unless a scene beat says it stops.
- Seat changes require the car to stop or an awkward on-page movement.

## Characters

| Name | Role | Current state | Must not change |
| --- | --- | --- | --- |
| Chen Yi | driver | tense, watching traffic | cannot turn fully around while driving |
| Luo Nan | front passenger | holding a paper envelope | cannot be in rear seat unless she exits/re-enters or climbs over |
| Xu Bei | rear-left passenger | left wrist bandaged | injury limits grip |
| Mei | rear-right passenger | wearing short skirt and flat shoes | outfit cannot become long skirt or heels without change beat |

## Occupancy and Capacity

| Resource | Mode | Capacity rule | Current occupants/items | Access path | Last confirmed |
| --- | --- | --- | --- | --- | --- |
| driver seat | one-person seat | one driver | Chen Yi | driver door | scene start |
| front passenger seat | one-person seat | one passenger | Luo Nan, paper envelope in lap | front passenger door | scene start |
| rear-left seat | one-person seat unless changed on-page | one passenger | Xu Bei | rear-left door | scene start |
| rear-right seat | one-person seat unless changed on-page | one passenger | Mei, small shoulder bag | rear-right door | scene start |
| rear bench as whole | separated seats, not bed | three seated passengers if rear-center is open | Xu Bei, Mei; rear-center empty | rear doors | scene start |

## Spatial Blocking

| Character | Position | Facing | Can see/reach | Blocked by | Last confirmed |
| --- | --- | --- | --- | --- | --- |
| Chen Yi | driver seat | forward | steering wheel, rearview mirror, gear shift | seat belt, traffic | scene start |
| Luo Nan | front passenger seat | forward/right window | glove box, envelope, dashboard, Chen Yi's arm | seat belt, center console | scene start |
| Xu Bei | rear-left seat | forward | left door, rear window, Mei if leaning | front seat back, bandaged wrist | scene start |
| Mei | rear-right seat | forward | right door, Xu Bei if leaning | front seat back, short skirt limits large movement | scene start |

## Appearance and Props

| Character | Clothing | Shoes | Hair/makeup | Injuries/body state | Carried items | Last confirmed |
| --- | --- | --- | --- | --- | --- | --- |
| Chen Yi | gray jacket | dark sneakers | wet hair at temples | tired eyes | car keys, phone in console | scene start |
| Luo Nan | beige coat over blue dress | flat ankle boots | hair clipped up | none | paper envelope in lap | scene start |
| Xu Bei | black hoodie | canvas shoes | hair damp | left wrist bandaged | cracked phone | scene start |
| Mei | short skirt, oversized sweater | flat shoes | lipstick smudged | cold hands | small shoulder bag | scene start |

## Movement Log

| Beat | Character | From | To | Transition shown |
| --- | --- | --- | --- | --- |
| 0 | everyone | outside prior scene | listed seats | established at scene start |

## Active Threads

- Luo Nan is hiding what is inside the envelope.
- Xu Bei saw someone follow them before they got in the car.
- Mei wants to leave but has not said so directly.

## Voice Anchors

- Close third person around Luo Nan.
- Tight physical blocking; no casual seat changes.
- Rain, glass, seat belts, and mirrors should shape what people can see.

## Current State

- The sedan is moving through slow traffic.
- Chen Yi is driving.
- Luo Nan remains in the front passenger seat.
- Xu Bei remains rear-left.
- Mei remains rear-right in short skirt and flat shoes.

## Do Not Forget

- No one can move from front to rear without a visible transition.
- Mei's outfit is short skirt plus flat shoes.
- Xu Bei's left wrist is bandaged.
- Luo Nan's envelope is in her lap unless moved on-page.
