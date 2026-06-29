---
name: "collection-pipeline"
description: "Collection Pipeline 集合管道 -- Functional设计模式。Learn how the Collection Pipeline design pattern in Java enhances data processing by chaining operations in a sequence. This pattern promotes a declar"
url: "https://java-design-patterns.com/patterns/collection-pipeline/"
category: "functional"
tags: [Reactive, Data transformation, Data processing, Functional decomposition]
---

# Collection Pipeline 集合管道模式

> 官方文档: https://java-design-patterns.com/patterns/collection-pipeline/
> 分类: Functional (functional)
> 标签: Reactive, Data transformation, Data processing, Functional decomposition

FunctionalFunctional decompositionData processingData transformationReactiveAbout 3 min

* * *

## [Intent of Collection Pipeline Design Pattern](https://java-design-patterns.com/patterns/collection-pipeline/#intent-of-collection-pipeline-design-pattern)

The Collection Pipeline design pattern in Java processes collections of data by chaining operations in a sequence. Utilizing the Java Stream API, it transforms data declaratively, focusing on what should be done rather than how.

## [Detailed Explanation of Collection Pipeline Pattern with Real-World Examples](https://java-design-patterns.com/patterns/collection-pipeline/#detailed-explanation-of-collection-pipeline-pattern-with-real-world-examples)

Real-world example

> Imagine a real-world example of a factory assembly line for manufacturing cars. In this assembly line, each station performs a specific task on the car chassis, such as installing the engine, painting the body, attaching the wheels, and inspecting the final product. Each station takes the output from the previous station and adds its own processing step. This sequence of operations is analogous to the Collection Pipeline design pattern, where each step in the pipeline transforms the data and passes it on to the next step, ensuring an efficient and organized workflow.

In plain words

> The Collection Pipeline pattern in Java involves processing data through a series of operations using the Stream API. Each operation transforms the data in sequence, akin to an assembly line in a factory, promoting functional programming principles.

Wikipedia says

> In software engineering, a pipeline consists of a chain of processing elements (processes, threads, coroutines, functions, etc.), arranged so that the output of each element is the input of the next; the name is by analogy to a physical pipeline. Usually some amount of buffering is provided between consecutive elements. The information that flows in these pipelines is often a stream of records, bytes, or bits, and the elements of a pipeline may be called filters; this is also called the pipe(s) and filters design pattern. Connecting elements into a pipeline is analogous to function composition.

Flowchart

![Collection Pipeline flowchart](https://java-design-patterns.com/assets/img/collection-pipeline-flowchart.8c45285b.png)

## [Programmatic Example of Collection Pipeline Pattern in Java](https://java-design-patterns.com/patterns/collection-pipeline/#programmatic-example-of-collection-pipeline-pattern-in-java)

The Collection Pipeline is a programming pattern where you organize some computation as a sequence of operations which compose by taking a collection as output of one operation and feeding it into the next.

Here's a programmatic example of the Collection Pipeline design pattern:

**Step 1: Filtering**

We start with a list of `Car` objects and we want to filter out those that were manufactured after the year 2000. This is done using the `stream()` method to create a stream from the list, the `filter()` method to filter out the cars we want, and the `collect()` method to collect the results into a new list.

```java
public static List<String> getModelsAfter2000(List<Car> cars){
    return cars.stream()
        .filter(car -> car.getYear() > 2000) // Filter cars manufactured after 2000
        .sorted(comparing(Car::getYear)) // Sort the cars by year
        .map(Car::getModel) // Get the model of each car
        .collect(toList()); // Collect the results into a new list
}
```

**Step 2: Grouping**

Next, we want to group the cars by their category. This is done using the `groupingBy` collector.

```java
public static Map<Category, List<Car>> getGroupingOfCarsByCategory(List<Car> cars){
    return cars.stream()
        .collect(groupingBy(Car::getCategory)); // Group cars by category
}
```

**Step 3: Filtering, Sorting and Transforming**

Finally, we want to filter the cars owned by a person to only include sedans, sort them by date, and then transform the sorted cars into a list of `Car` objects.

```java
public static List<Car> getSedanCarsOwnedSortedByDate(List<Person> persons){
    return persons.stream()
        .flatMap(person -> person.getCars().stream()) // Flatten the list of cars owned by each person
        .filter(car -> Category.SEDAN.equals(car.getCategory())) // Filter to only include sedans
        .sorted(comparing(Car::getDate)) // Sort the cars by date
        .collect(toList()); // Collect the results into a new list
}
```

In each of these methods, the Collection Pipeline pattern is used to perform a series of operations on the collection of cars in a declarative manner, which improves readability and maintainability.

## [When to Use the Collection Pipeline Pattern in Java](https://java-design-patterns.com/patterns/collection-pipeline/#when-to-use-the-collection-pipeline-pattern-in-java)

The Collection Pipeline pattern is ideal for Java developers handling bulk data operations, including filtering, mapping, sorting, and reducing collections, particularly with Java 8+ Stream API.

Use the Collection Pipeline pattern:

- When you need to perform a series of transformations on a collection of data.
- When you want to improve readability and maintainability of complex data processing code.
- When working with large datasets where intermediate results should not be stored in memory.

## [Real-World Applications of Collection Pipeline Pattern in Java](https://java-design-patterns.com/patterns/collection-pipeline/#real-world-applications-of-collection-pipeline-pattern-in-java)

- LINQ in .NET
- Stream API in Java 8+
- Collections in modern functional languages (e.g., Haskell, Scala)
- Database query builders and ORM frameworks

## [Benefits and Trade-offs of Collection Pipeline Pattern](https://java-design-patterns.com/patterns/collection-pipeline/#benefits-and-trade-offs-of-collection-pipeline-pattern)

Benefits:

- Readability: The code is more readable and declarative, making it easier to understand the sequence of operations.
- Maintainability: Easier to modify or extend the pipeline with additional operations.
- Reusability: Common operations can be abstracted into reusable functions.
- Lazy Evaluation: Some implementations allow for operations to be lazily evaluated, improving performance.

Trade-offs:

- Performance Overhead: Chaining multiple operations can introduce overhead compared to traditional loops, especially for short pipelines or very large collections.
- Debugging Difficulty: Debugging a chain of operations might be more challenging due to the lack of intermediate variables.
- Limited to Collections: Primarily focused on collections, and its utility might be limited outside of collection processing.

## [Related Java Design Patterns](https://java-design-patterns.com/patterns/collection-pipeline/#related-java-design-patterns)

- [Builder](https://java-design-patterns.com/patterns/builder/): Similar fluent interface style but used for object construction.
- [Chain of Responsibility](https://java-design-patterns.com/patterns/chain-of-responsibility/): Conceptually similar in chaining handlers, but applied to object requests rather than data collection processing.
- [Strategy](https://java-design-patterns.com/patterns/strategy/): Can be used within a pipeline stage to encapsulate different algorithms that can be selected at runtime.

## [References and Credits](https://java-design-patterns.com/patterns/collection-pipeline/#references-and-credits)

- [Functional Programming in Scala](https://amzn.to/4cEo6K2)
- [Java 8 in Action: Lambdas, Streams, and functional-style programming](https://amzn.to/3THp4wy)
- [Refactoring: Improving the Design of Existing Code](https://amzn.to/3VDMWDO)
- [Collection Pipeline (Martin Fowler)](https://martinfowler.com/articles/collection-pipeline/)
