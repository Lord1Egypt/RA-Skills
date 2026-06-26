# Schema Generation Examples

Practical examples of deriving schemas from domain text across different domains.

## Example 1: University Domain

### Input Text

```
A university system manages students, professors, courses, and departments.
Each department belongs to a college and manages multiple professors and courses.
Students can enroll in courses taught by professors.
Courses have prerequisites that must be completed before enrollment.
Professors specialize in specific areas and teach courses.
```

### Generated Schema

**Entities:**
```
- University
- College
- Department
- Student
- Professor
- Course
```

**Relationships:**
```
- University -[HAS]-> College
- College -[HAS]-> Department
- Department -[MANAGES]-> Professor
- Department -[OFFERS]-> Course
- Professor -[TEACHES]-> Course
- Student -[ENROLLED_IN]-> Course
- Course -[REQUIRES]-> Course (prerequisite)
```

**Properties:**
```
University:
  - name: String
  - founded_year: Integer
  - location: String

College:
  - name: String
  - dean: String

Department:
  - name: String
  - budget: Float
  - chair: String

Student:
  - student_id: String
  - name: String
  - email: String
  - enrollment_date: Date

Professor:
  - professor_id: String
  - name: String
  - email: String
  - specialization: String

Course:
  - course_code: String
  - title: String
  - credits: Integer
  - description: String
```

---

## Example 2: E-Commerce Domain

### Input Text

```
An e-commerce platform connects customers, products, and orders.
Customers browse products organized in categories.
Products are supplied by multiple suppliers and have inventory information.
Customers can place orders containing multiple products.
Each order has a payment status and shipping status.
Products have reviews from customers.
```

### Generated Schema

**Entities:**
```
- Customer
- Product
- Category
- Supplier
- Order
- OrderItem
- Review
```

**Relationships:**
```
- Customer -[PLACES]-> Order
- Order -[CONTAINS]-> OrderItem
- OrderItem -[REFERS_TO]-> Product
- Product -[BELONGS_TO]-> Category
- Product -[SUPPLIED_BY]-> Supplier
- Supplier -[PROVIDES]-> Product
- Customer -[REVIEWS]-> Product
```

**Properties:**
```
Customer:
  - customer_id: String
  - name: String
  - email: String
  - phone: String
  - address: String

Product:
  - product_id: String
  - name: String
  - price: Float
  - sku: String
  - description: String
  - stock_quantity: Integer

Category:
  - category_id: String
  - name: String
  - parent_category: String

Supplier:
  - supplier_id: String
  - name: String
  - contact_email: String
  - rating: Float

Order:
  - order_id: String
  - customer_id: String
  - order_date: Date
  - total_amount: Float
  - payment_status: String
  - shipping_status: String

OrderItem:
  - order_item_id: String
  - product_id: String
  - quantity: Integer
  - unit_price: Float

Review:
  - review_id: String
  - rating: Integer
  - text: String
  - review_date: Date
```

---

## Example 3: Healthcare Domain

### Input Text

```
A hospital system manages patients, doctors, and departments.
Patients are diagnosed with conditions and receive treatments.
Doctors specialize in departments and treat patients.
Each treatment is prescribed by a doctor and administered by nurses.
Patients have medical records documenting diagnoses and treatments.
Hospitals have multiple departments with staff and equipment.
```

### Generated Schema

**Entities:**
```
- Hospital
- Department
- Doctor
- Nurse
- Patient
- Diagnosis
- Treatment
- MedicalRecord
- Equipment
```

**Relationships:**
```
- Hospital -[HAS]-> Department
- Doctor -[WORKS_IN]-> Department
- Nurse -[WORKS_IN]-> Department
- Patient -[DIAGNOSED_WITH]-> Diagnosis
- Doctor -[DIAGNOSES]-> Patient
- Doctor -[PRESCRIBES]-> Treatment
- Nurse -[ADMINISTERS]-> Treatment
- Patient -[RECEIVES]-> Treatment
- Patient -[HAS]-> MedicalRecord
- Department -[CONTAINS]-> Equipment
```

**Properties:**
```
Hospital:
  - hospital_id: String
  - name: String
  - location: String
  - beds_count: Integer

Department:
  - dept_id: String
  - name: String
  - head_doctor: String
  - budget: Float

Doctor:
  - doctor_id: String
  - name: String
  - email: String
  - specialization: String
  - license_number: String

Patient:
  - patient_id: String
  - name: String
  - dob: Date
  - blood_type: String
  - contact: String

Diagnosis:
  - diagnosis_id: String
  - disease_code: String
  - disease_name: String
  - icd_code: String

Treatment:
  - treatment_id: String
  - name: String
  - description: String
  - cost: Float

Equipment:
  - equipment_id: String
  - name: String
  - model: String
  - purchase_date: Date
```

---

## Example 4: Social Network Domain

### Input Text

```
A social network connects users who can follow each other.
Users create posts and interact through comments and likes.
Posts can be shared by users and tagged with hashtags.
Users can form groups and invite other users.
Each user has a profile with personal information.
Users can send messages to each other.
```

### Generated Schema

**Entities:**
```
- User
- Post
- Comment
- Like
- Group
- Message
- Hashtag
- Profile
```

**Relationships:**
```
- User -[FOLLOWS]-> User
- User -[CREATES]-> Post
- User -[COMMENTS_ON]-> Post
- User -[LIKES]-> Post
- Post -[TAGGED_WITH]-> Hashtag
- User -[MEMBER_OF]-> Group
- Group -[CREATED_BY]-> User
- User -[SENDS_MESSAGE]-> User
- User -[HAS_PROFILE]-> Profile
```

**Properties:**
```
User:
  - user_id: String
  - username: String
  - email: String
  - joined_date: Date

Profile:
  - user_id: String
  - bio: String
  - location: String
  - profile_picture_url: String

Post:
  - post_id: String
  - content: String
  - created_date: Date
  - likes_count: Integer
  - comments_count: Integer

Comment:
  - comment_id: String
  - content: String
  - created_date: Date

Group:
  - group_id: String
  - name: String
  - description: String
  - member_count: Integer

Message:
  - message_id: String
  - content: String
  - timestamp: Date
  - read: Boolean

Hashtag:
  - tag_id: String
  - tag_name: String
  - usage_count: Integer
```

---

## Quick Reference

### Schema Elements Summary

| Domain | Entities | Relationships | Avg Properties |
|--------|----------|---------------|-----------------|
| University | 6 | 7 | 4-5 |
| E-Commerce | 7 | 8 | 4-6 |
| Healthcare | 9 | 10 | 4-7 |
| Social Network | 8 | 9 | 3-5 |

### Naming Conventions Used

- **Entities:** PascalCase (Student, Course)
- **Relationships:** SCREAMING_SNAKE_CASE (ENROLLED_IN, TEACHES)
- **Properties:** snake_case (student_id, enrollment_date)
- **Directions:** Left → Right (Student → Course)

See [extraction-patterns.md](../references/extraction-patterns.md) for detailed extraction guidelines.

