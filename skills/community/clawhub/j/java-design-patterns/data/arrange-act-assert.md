[Skip to main content](https://java-design-patterns.com/patterns/arrange-act-assert/#main-content)

# Arrange/Act/Assert Pattern in Java: Enhance Testing Clarity and Simplicity

TestingCode simplificationIsolationTestingAbout 2 min

* * *

## [Also known as](https://java-design-patterns.com/patterns/arrange-act-assert/\#also-known-as)

- Given/When/Then

## [Intent of Arrange/Act/Assert Design Pattern](https://java-design-patterns.com/patterns/arrange-act-assert/\#intent-of-arrange-act-assert-design-pattern)

The Arrange/Act/Assert pattern is essential in unit testing in Java. This testing method structures unit tests clearly by dividing them into three distinct sections: setup (Arrange), execution (Act), and verification (Assert).

## [Detailed Explanation of Arrange/Act/Assert Pattern with Real-World Examples](https://java-design-patterns.com/patterns/arrange-act-assert/\#detailed-explanation-of-arrange-act-assert-pattern-with-real-world-examples)

Real-world example

> Imagine you are organizing a small event. To ensure everything runs smoothly, you follow a pattern similar to Arrange/Act/Assert:
>
> 1. **Arrange**: You set up the venue, prepare the guest list, arrange seating, and organize the catering.
> 2. **Act**: You conduct the event according to the plan, welcoming guests, serving food, and following the schedule.
> 3. **Assert**: After the event, you evaluate its success by checking guest feedback, ensuring all tasks were completed, and reviewing if everything went as planned.
>
> This clear separation of preparation, execution, and evaluation helps ensure the event is well-organized and successful, mirroring the structured approach of the Arrange/Act/Assert pattern in software testing.

In plain words

> Arrange/Act/Assert is a testing pattern that organizes tests into three clear steps for easy maintenance.

WikiWikiWeb says

> Arrange/Act/Assert is a pattern for arranging and formatting code in UnitTest methods.

Flowchart

![Arrange/Act/Assert flowchart](https://java-design-patterns.com/assets/img/arrange-act-assert-flowchart.367e6a0f.png)

## [Programmatic Example of Arrange/Act/Assert Pattern in Java](https://java-design-patterns.com/patterns/arrange-act-assert/\#programmatic-example-of-arrange-act-assert-pattern-in-java)

We need to write comprehensive and clear unit test suite for a class. Using the Arrange/Act/Assert pattern in Java testing ensures clarity.

Let's first introduce our `Cash` class to be unit tested.

```java
public class Cash {

    private int amount;

    Cash(int amount) {
        this.amount = amount;
    }

    void plus(int addend) {
        amount += addend;
    }

    boolean minus(int subtrahend) {
        if (amount >= subtrahend) {
            amount -= subtrahend;
            return true;
        } else {
            return false;
        }
    }

    int count() {
        return amount;
    }
}
```

Then we write our unit tests according to Arrange/Act/Assert pattern. Notice the clearly separated steps for each unit test.

```java
class CashAAATest {

    @Test
    void testPlus() {
        //Arrange
        var cash = new Cash(3);
        //Act
        cash.plus(4);
        //Assert
        assertEquals(7, cash.count());
    }

    @Test
    void testMinus() {
        //Arrange
        var cash = new Cash(8);
        //Act
        var result = cash.minus(5);
        //Assert
        assertTrue(result);
        assertEquals(3, cash.count());
    }

    @Test
    void testInsufficientMinus() {
        //Arrange
        var cash = new Cash(1);
        //Act
        var result = cash.minus(6);
        //Assert
        assertFalse(result);
        assertEquals(1, cash.count());
    }

    @Test
    void testUpdate() {
        //Arrange
        var cash = new Cash(5);
        //Act
        cash.plus(6);
        var result = cash.minus(3);
        //Assert
        assertTrue(result);
        assertEquals(8, cash.count());
    }
}
```

## [When to Use the Arrange/Act/Assert Pattern in Java](https://java-design-patterns.com/patterns/arrange-act-assert/\#when-to-use-the-arrange-act-assert-pattern-in-java)

Use Arrange/Act/Assert pattern when

- Unit testing, especially within the context of TDD and BDD
- Anywhere clarity and structure are needed in test cases

## [Real-World Applications of Arrange/Act/Assert Pattern in Java](https://java-design-patterns.com/patterns/arrange-act-assert/\#real-world-applications-of-arrange-act-assert-pattern-in-java)

- This pattern is particularly useful when practicing TDD and/or BDD methodologies in Java.
- Utilized in various programming languages and testing frameworks, such as JUnit (Java), NUnit (.NET), and xUnit frameworks.

## [Benefits and Trade-offs of Arrange/Act/Assert Pattern](https://java-design-patterns.com/patterns/arrange-act-assert/\#benefits-and-trade-offs-of-arrange-act-assert-pattern)

Benefits:

- Improved readability of tests by clearly separating the setup, action, and verification steps.
- Easier maintenance and understanding of tests, as each test is structured in a predictable way.
- Facilitates debugging by isolating test failures to specific phases within the test.

Trade-offs:

- May introduce redundancy in tests, as similar arrangements may be repeated across tests.
- Some complex tests might not fit neatly into this structure, requiring additional context or setup outside these three phases.

## [Related Java Design Patterns](https://java-design-patterns.com/patterns/arrange-act-assert/\#related-java-design-patterns)

- [Page Object](https://java-design-patterns.com/patterns/page-object/): A pattern for organizing UI tests that can be used in conjunction with Arrange/Act/Assert.

## [References and Credits](https://java-design-patterns.com/patterns/arrange-act-assert/\#references-and-credits)

- [The Art of Unit Testing: with examples in C#](https://amzn.to/49IbdwO)
- [Test Driven Development: By Example](https://amzn.to/3wEwKbF)
- [Unit Testing Principles, Practices, and Patterns: Effective testing styles, patterns, and reliable automation for unit testing, mocking, and integration testing with examples in C#](https://amzn.to/4ayjpiM)
- [xUnit Test Patterns: Refactoring Test Code](https://amzn.to/4dHGDpm)
- [Arrange, Act, Assert: What is AAA Testing?](https://blog.ncrunch.net/post/arrange-act-assert-aaa-testing.aspx)
- [Bill Wake: 3A – Arrange, Act, Assert (NCrunch)](https://xp123.com/articles/3a-arrange-act-assert/)
- [GivenWhenThen (Martin Fowler)](https://martinfowler.com/bliki/GivenWhenThen.html)