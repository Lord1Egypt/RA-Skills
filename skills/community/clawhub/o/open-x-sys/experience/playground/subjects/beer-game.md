# Materials: the beer game

[Chinese edition](https://github.com/gengshupeng/open-x-sys/blob/main/skills/open-x-sys.zh-CN/experience/playground/subjects/beer-game.md)

> **A ready subject for the Playground: a classic problem.**
> **Status of these materials**: written on 2026-11-16 from published sources, from memory of those sources, and **not yet verified against the primary texts**. Each item carries a confidence mark. The game's parameters vary slightly between versions; the classic values are given.
> **These are materials, not conclusions.** They describe the game and what is observed when people play it. Why it happens and what would stop it are for the run to find.

Confidence marks: **[A]** well established and widely reported · **[B]** reported by a named source, worth checking · **[C]** approximate or version-dependent.

## The game

- **[A]** The beer distribution game was developed at the MIT Sloan School of Management in the 1960s by the system dynamics group founded by Jay Forrester, and has been played by very large numbers of students and managers since.
- **[A]** Four positions form a supply chain for one product: **retailer**, **wholesaler**, **distributor**, **factory**. Each is played by a person or a small team.
- **[A]** Each week, every position receives incoming orders from the position downstream, ships what it can from inventory, receives shipments ordered earlier, and decides how much to order from the position upstream. The factory decides how much to produce.
- **[A]** Orders travel upstream and goods travel downstream, both with delays. **[C]** In the classic board version there is a delay of about two weeks for orders to arrive and two weeks for shipments, and about three weeks for production.
- **[C]** Costs are charged each week: 0.50 dollars per case held in inventory and 1.00 dollar per case of unfilled orders (backlog). The team's goal is to minimize total cost for the whole chain.
- **[A]** Players may not communicate. The only information that passes between positions is the orders themselves. Only the retailer sees customer demand.
- **[C]** In the classic scenario customer demand is 4 cases a week for the first weeks, rises once to 8 cases a week, and stays there for the rest of the game. Players are not told this in advance.

## What is observed

- **[A]** Orders and inventories oscillate: a period of shortage and backlog is followed by a period of large excess inventory.
- **[A]** The swings get larger at each step upstream. The factory's swings are the largest.
- **[A]** The peaks arrive later at each step upstream.
- **[B]** John Sterman (1989) reported that average team costs were about ten times those of a benchmark ordering rule.
- **[B]** In debriefings, most players attribute what happened to customer demand, and are surprised to learn that it changed only once.
- **[B]** Sterman's analysis found that players responded to their current inventory and largely ignored the orders they had already placed that had not yet arrived.
- **[A]** The same pattern appears across groups of students, experienced managers and executives.

## The same pattern in real supply chains

- **[A]** Hau Lee, V. Padmanabhan and Seungjin Whang (1997) described the "bullwhip effect": the variability of orders increases as one moves up a supply chain from consumers to manufacturers and suppliers.
- **[B]** A much-cited example is Procter and Gamble's observation that consumer purchases of diapers were steady while distributors' orders varied widely and orders to suppliers varied more.
- **[A]** Lee and colleagues identified four causes that operate even when everyone acts rationally: updating forecasts from orders received; batching of orders; price promotions that lead buyers to stock up; and over-ordering when supply is rationed.
- **[A]** Measures used in practice include sharing point-of-sale data along the chain, vendor-managed inventory, shorter lead times, smaller and more frequent orders, and stable pricing.

## Numbers worth sizing for yourself

- With four positions and four weeks between placing an order and receiving it at each, how long does a change at the retailer take to be felt at the factory?
- If each position, seeing orders rise, adds a safety margin of 20 percent, what increase reaches the factory?
- With the cost figures above, what does a backlog of 40 cases lasting five weeks cost against holding 40 extra cases for five weeks?

## Points where accounts differ

- How much of the effect is behavioural (misjudging delays) and how much is structural (rational responses to batching, pricing and rationing).
- Whether more information alone removes it, or whether incentives and contracts must change as well.

## Primary and standard sources

- Jay W. Forrester, *Industrial Dynamics* (MIT Press, 1961).
- John D. Sterman, "Modeling Managerial Behavior: Misperceptions of Feedback in a Dynamic Decision Making Experiment", *Management Science* 35(3), 1989.
- Hau L. Lee, V. Padmanabhan and Seungjin Whang, "The Bullwhip Effect in Supply Chains", *Sloan Management Review* (Spring 1997); and "Information Distortion in a Supply Chain: The Bullwhip Effect", *Management Science* 43(4), 1997.
- John D. Sterman, *Business Dynamics* (2000), chapters on supply chains and oscillation.
- Peter Senge, *The Fifth Discipline* (1990), which describes a session of the game.
