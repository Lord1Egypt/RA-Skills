# Essential Java Design Principles for Developers

## Introduction to Programming Principles

There are certain universal laws and principles in software development that guide architects, programmers, and anyone needing to design software.

## [KISS](https://java-design-patterns.com/principles/#kiss)

Most systems work best if they are kept simple rather than made complex.

Why

- Less code takes less time to write, has less bugs, and is easier to modify.
- Simplicity is the ultimate sophistication.

## [YAGNI](https://java-design-patterns.com/principles/#yagni)

YAGNI stands for "you aren't gonna need it": don't implement something until it is necessary.

Why

- Any work that's only used for a feature that's needed tomorrow, means losing effort from features that need to be done for the current iteration.
- It leads to code bloat; the software becomes larger and more complicated.

How

- Always implement things when you actually need them, never when you just foresee that you need them.

## [Do The Simplest Thing That Could Possibly Work](https://java-design-patterns.com/principles/#do-the-simplest-thing-that-could-possibly-work)

Why

- Real progress against the real problem is maximized if we just work on what the problem really is.

How

- Ask yourself: "What is the simplest thing that could possibly work?"

## [Separation of Concerns](https://java-design-patterns.com/principles/#separation-of-concerns)

Separation of concerns is a design principle for separating a computer program into distinct sections, such that each section addresses a separate concern. For example the business logic of the application is a concern and the user interface is another concern.

Why

- Simplify development and maintenance of software applications.
- When concerns are well-separated, individual sections can be reused, as well as developed and updated independently.

How

- Break program functionality into separate modules that overlap as little as possible.

## [Keep things DRY](https://java-design-patterns.com/principles/#keep-things-dry)

Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.

Why

- Duplication can lead to maintenance nightmares, poor factoring, and logical contradictions.

How

- Put business rules, long expressions, if statements, math formulas, metadata, etc. in only one place.
- Apply the Rule of three.

## [Code For The Maintainer](https://java-design-patterns.com/principles/#code-for-the-maintainer)

Why

- Maintenance is by far the most expensive phase of any project.

How

- Always code as if the person who ends up maintaining your code is a violent psychopath who knows where you live.

## [Avoid Premature Optimization](https://java-design-patterns.com/principles/#avoid-premature-optimization)

Quoting Donald Knuth: "Premature optimization is the root of all evil."

Why

- It is unknown upfront where the bottlenecks will be.
- After optimization, it might be harder to read and thus maintain.

How

- Make It Work Make It Right Make It Fast

## [Minimise Coupling](https://java-design-patterns.com/principles/#minimise-coupling)

Coupling between modules/components is their degree of mutual interdependence; lower coupling is better.

Why

- A change in one module usually forces a ripple effect of changes in other modules.

How

- Eliminate, minimise, and reduce complexity of necessary relationships.
- Apply the Law of Demeter.

## [Law of Demeter](https://java-design-patterns.com/principles/#law-of-demeter)

Don't talk to strangers.

How

A method of an object may only call methods of:
1. The object itself.
2. An argument of the method.
3. Any object created within the method.
4. Any direct properties/fields of the object.

## [Composition Over Inheritance](https://java-design-patterns.com/principles/#composition-over-inheritance)

Why

- Less coupling between classes.
- Using inheritance, subclasses easily make assumptions, and break LSP.

How

- Compose when there is a "has a" relationship, inherit when "is a".

## [Orthogonality](https://java-design-patterns.com/principles/#orthogonality)

Things that are not related conceptually should not be related in the system. The more orthogonal the design, the fewer exceptions.

## [Robustness Principle](https://java-design-patterns.com/principles/#robustness-principle)

Be conservative in what you do, be liberal in what you accept from others.

## [Inversion of Control](https://java-design-patterns.com/principles/#inversion-of-control)

Also known as the Hollywood Principle, "Don't call us, we'll call you". Custom-written portions receive the flow of control from a generic framework.

How

- Using Factory pattern, Service Locator pattern, Dependency Injection, Template Method pattern, Strategy pattern.

## [Maximise Cohesion](https://java-design-patterns.com/principles/#maximise-cohesion)

Cohesion of a single module/component is the degree to which its responsibilities form a meaningful unit; higher cohesion is better.

## [Liskov Substitution Principle](https://java-design-patterns.com/principles/#liskov-substitution-principle)

Objects in a program should be replaceable with instances of their subtypes without altering the correctness of that program.

## [Open/Closed Principle](https://java-design-patterns.com/principles/#open-closed-principle)

Software entities should be open for extension, but closed for modification.

## [Single Responsibility Principle](https://java-design-patterns.com/principles/#single-responsibility-principle)

A class should never have more than one reason to change.

## [Hide Implementation Details](https://java-design-patterns.com/principles/#hide-implementation-details)

A software module hides information by providing an interface, and not leak any unnecessary information.

## [Curly's Law](https://java-design-patterns.com/principles/#curly-s-law)

Do One Thing. Choose a single, clearly defined goal for any particular bit of code.

## [Encapsulate What Changes](https://java-design-patterns.com/principles/#encapsulate-what-changes)

A good design identifies the hotspots that are most likely to change and encapsulates them behind an API.

## [Interface Segregation Principle](https://java-design-patterns.com/principles/#interface-segregation-principle)

Reduce fat interfaces into multiple smaller and more specific client specific interfaces.

## [Boy-Scout Rule](https://java-design-patterns.com/principles/#boy-scout-rule)

Leave the campground cleaner than you found it. Always leave the code cleaner than we found it.

## [Command Query Separation](https://java-design-patterns.com/principles/#command-query-separation)

Each method should be either a command that performs an action or a query that returns data to the caller but not both. Asking a question should not modify the answer.

## [Murphy's Law](https://java-design-patterns.com/principles/#murphy-s-law)

Anything that can go wrong will go wrong.

## [Brooks's Law](https://java-design-patterns.com/principles/#brooks-s-law)

Adding manpower to a late software project makes it later.

## [Linus's Law](https://java-design-patterns.com/principles/#linus-s-law)

Given enough eyeballs, all bugs are shallow.
