## Purpose

Central repository for ALL code templates, algorithmic patterns, and reusable instructional structures.

**Constraint:** This is the ONLY file that may contain code templates, pseudocode, and structured algorithmic patterns. No other file in this project shall contain code templates or pseudocode.

---

## Section A: Instructional Strategy Templates

### Template A-1: Direct Instruction Pattern

**Purpose:** Deliver structured factual content with clear objectives, sequential explanation, and embedded formative checks. Optimized for introductory topics and foundational knowledge transfer.

**Input Parameters:**
- `subject` (string): The academic subject (e.g., "Mathematics", "History")
- `topic` (string): The specific topic within the subject
- `grade_level` (integer): Target grade level, range [1, 12]
- `time_allocation` (integer): Minutes allocated for the instruction session

**Output:** Structured lesson plan containing objectives, teaching sequence, embedded assessments, and tier assignment

**Pseudocode:**

```
FUNCTION DirectInstruction(subject, topic, grade_level, time_allocation):
    // Phase 1: Diagnose
    learner_profile <- AssessLearnerState(grade_level, subject)
    tier <- AssignTier(learner_profile)

    // Phase 2: Select
    objectives <- GenerateObjectives(topic, grade_level, tier)
    sequence <- BuildLessonSequence(objectives, time_allocation)

    // Phase 3: Deliver
    FOR EACH segment IN sequence:
        content <- RetrieveContent(segment.topic, grade_level)
        explanation <- GenerateExplanation(content, tier)
        DeliverToLearner(explanation)

        // Phase 4: Assess (embedded checkpoint)
        check_item <- GenerateCheckItem(segment.objective)
        response <- GetLearnerResponse(check_item)
        IF NOT PassesAssessment(response, segment.objective):
            // Phase 5: Remediate
            remediation <- GenerateRemediation(segment.objective, response)
            DeliverToLearner(remediation)
            REPEAT segment

    RETURN LessonPlan {
        objectives: objectives,
        sequence: sequence,
        assessments: collected_assessments,
        tier: tier
    }
END FUNCTION
```

---

### Template A-2: Inquiry-Based Learning Pattern

**Purpose:** Facilitate student-driven exploration through structured inquiry cycles. The agent poses a driving question and guides learners through hypothesis formation, investigation, and conclusion drawing.

**Input Parameters:**
- `subject` (string): The academic subject
- `driving_question` (string): The open-ended question that anchors the inquiry
- `grade_level` (integer): Target grade level, range [1, 12]

**Output:** Inquiry sequence containing hypothesis prompts, investigation steps, data analysis guidance, and conclusion framework

**Pseudocode:**

```
FUNCTION InquiryBasedLearning(subject, driving_question, grade_level):
    // Phase 1: Diagnose
    learner_profile <- AssessLearnerState(grade_level, subject)
    tier <- AssignTier(learner_profile)

    // Phase 2: Select
    inquiry_design <- DesignInquiry(driving_question, grade_level, tier)

    // Phase 3: Deliver
    // Step 1: Launch
    PresentDrivingQuestion(driving_question)
    ActivatePriorKnowledge(subject, grade_level)

    // Step 2: Hypothesize
    hypotheses <- CollectHypotheses(learner_profile.size)
    FOR EACH hypothesis IN hypotheses:
        ValidateForm(hypothesis)
        Log(hypothesis)

    // Step 3: Investigate
    investigation_plan <- DesignInvestigation(inquiry_design)
    resources <- GatherResources(investigation_plan)
    FOR EACH step IN investigation_plan.steps:
        DeliverGuidance(step, resources)
        student_output <- CollectStudentWork(step)
        IF NOT MeetsCriteria(student_output, step.rubric):
            ProvideFeedback(student_output, step.rubric)

    // Step 4: Conclude
    conclusions <- SynthesizeFindings(collected_data)
    PresentConclusions(conclusions)

    // Phase 4: Assess
    assessment <- GenerateInquiryAssessment(inquiry_design)
    grade <- EvaluateAssessment(assessment)

    // Phase 5: Remediate
    IF grade < threshold:
        remediation <- DesignRemediation(inquiry_design, grade)
        ExecuteRemediation(remediation)

    RETURN InquiryReport {
        driving_question: driving_question,
        hypotheses: hypotheses,
        investigation: investigation_plan,
        conclusions: conclusions,
        assessment: assessment
    }
END FUNCTION
```

---

### Template A-3: Differentiated Instruction Pattern

**Purpose:** Provide three-tier differentiated task sets based on learner performance bands (below level, at level, above level). Ensures appropriate challenge for every learner.

**Input Parameters:**
- `learner_performance_band` (string): One of "below_level", "at_level", "above_level"
- `subject` (string): The academic subject
- `topic` (string): The specific topic

**Output:** Three-tier differentiated task set with scaffolding levels and extension activities

**Pseudocode:**

```
FUNCTION DifferentiatedInstruction(learner_performance_band, subject, topic):
    // Phase 1: Diagnose
    learners <- GetClassRoster()
    profiles <- MapPerformanceBands(learners)

    // Phase 2: Select
    base_objectives <- GenerateObjectives(topic, grade_level)

    // Phase 3: Deliver -- Branch by performance band
    differentiated_tasks <- {}

    IF learner_performance_band == "below_level":
        tasks <- DesignBelowLevelTasks(base_objectives)
        tasks.scaffolding <- Level(4)  // Maximum support
        tasks.modifications <- ApplyAccommodations(tasks)
    ELSE IF learner_performance_band == "at_level":
        tasks <- DesignAtLevelTasks(base_objectives)
        tasks.scaffolding <- Level(2)  // Moderate support
        tasks.modifications <- ApplyStandardDelivery(tasks)
    ELSE IF learner_performance_band == "above_level":
        tasks <- DesignAboveLevelTasks(base_objectives)
        tasks.scaffolding <- Level(0)  // Minimal support
        tasks.extensions <- AddEnrichment(tasks)

    differentiated_tasks[learner_performance_band] <- tasks

    // Deliver to each band
    FOR EACH band IN ["below_level", "at_level", "above_level"]:
        IF differentiated_tasks[band] EXISTS:
            DeliverTasks(differentiated_tasks[band])

    // Phase 4: Assess
    assessments <- GenerateBandAlignedAssessments(differentiated_tasks)
    FOR EACH assessment IN assessments:
        Evaluate(assessment)

    // Phase 5: Remediate
    FOR EACH learner IN learners:
        band <- GetPerformanceBand(learner)
        score <- GetAssessmentScore(learner)
        IF score < mastery_threshold:
            remediation <- DesignRemediation(band, score)
            ExecuteRemediation(remediation)

    RETURN DifferentiatedPlan {
        tasks: differentiated_tasks,
        assessments: assessments,
        remediation_plan: collected_remediations
    }
END FUNCTION
```

---

### Template A-4: Socratic Dialogue Pattern

**Purpose:** Generate sequenced question chains using adaptive questioning to probe learner understanding at specified Bloom taxonomy cognitive levels.

**Input Parameters:**
- `topic` (string): The subject topic under discussion
- `target_cognitive_level` (string): Bloom taxonomy level -- "remember", "understand", "apply", "analyze", "evaluate", "create"
- `learner_response_history` (list): Previous learner responses for adaptive branching

**Output:** Sequenced question chain with expected response patterns and adaptive branching logic

**Pseudocode:**

```
FUNCTION SocraticDialogue(topic, target_cognitive_level, learner_response_history):
    // Phase 1: Diagnose
    current_level <- AnalyzeResponseHistory(learner_response_history)
    gap <- IdentifyGap(current_level, target_cognitive_level)

    // Phase 2: Select
    question_chain <- GenerateQuestionChain(topic, target_cognitive_level, gap)

    // Phase 3: Deliver -- Adaptive questioning loop
    FOR EACH question IN question_chain:
        PresentQuestion(question)

        // Phase 4: Assess (real-time)
        response <- GetLearnerResponse()
        quality <- EvaluateResponse(response, question.rubric)

        IF quality >= proficient:
            RecordSuccess(response)
            IF question IS LAST:
                BREAK  // Chain complete
            ELSE:
                CONTINUE  // Next question in chain
        ELSE:
            // Adaptive branch: scaffold or redirect
            IF gap > 2 cognitive_levels:
                // Too large a gap -- step back
                scaffold_question <- GenerateScaffold(question, level=-1)
                PresentQuestion(scaffold_question)
                response <- GetLearnerResponse()
                IF Passes(response, scaffold_question.rubric):
                    CONTINUE  // Retry original question
                ELSE:
                    // Phase 5: Remediate
                    RemediateConcept(question.prerequisite_concept)
                    CONTINUE
            ELSE:
                // Provide hint and retry
                hint <- GenerateHint(question)
                PresentHint(hint)
                CONTINUE  // Retry same question

    // Phase 4: Summative Assessment
    final_assessment <- GenerateSummativeCheck(question_chain.topics)
    Evaluate(final_assessment)

    RETURN DialogueRecord {
        question_chain: question_chain,
        responses: collected_responses,
        adaptations: recorded_adaptations,
        assessment: final_assessment
    }
END FUNCTION
```

---

### Template A-5: Scaffolded Problem-Solving Pattern

**Purpose:** Provide step-by-step guided problem solving with configurable scaffold depth that fades support as learner competence increases.

**Input Parameters:**
- `subject` (string): The academic subject
- `problem_type` (string): Category of problem (e.g., "linear_equation", "essay_analysis", "experiment_design")
- `scaffold_depth` (integer): Scaffold intensity, range [1, 4] where 1=full support, 4=minimal support

**Output:** Step-by-step guided solution with fading support levels

**Pseudocode:**

```
FUNCTION ScaffoldedProblemSolving(subject, problem_type, scaffold_depth):
    // Phase 1: Diagnose
    learner_profile <- AssessLearnerState(grade_level, subject)
    current_competence <- EstimateCompetence(learner_profile, problem_type)

    // Phase 2: Select
    scaffold_level <- MapDepthToScaffold(scaffold_depth, current_competence)
    problem <- GenerateProblem(problem_type, grade_level)

    // Phase 3: Deliver -- Scaffolded solution path
    solution_steps <- DecomposeProblem(problem)

    FOR i, step IN solution_steps:
        IF scaffold_level >= 4:
            // Minimal support: learner attempts independently
            PresentStepPrompt(step)
            learner_attempt <- GetLearnerAttempt(step)
            feedback <- GenerateFeedback(step, learner_attempt, level="minimal")
            DeliverFeedback(feedback)

        ELSE IF scaffold_level >= 2:
            // Moderate support: guided hints
            PresentPartialSolution(step, hint_level=scaffold_level)
            learner_fill <- GetLearnerCompletion(step)
            IF NOT Correct(learner_fill, step):
                hint <- GenerateHint(step, depth=scaffold_level)
                Deliver(hint)
                REPEAT step

        ELSE:
            // Full support: worked example
            PresentWorkedExample(step)
            CheckUnderstanding(step)
            learner_response <- GetResponse()
            IF NOT Understands(learner_response):
                PresentAlternativeExplanation(step)

    // Phase 4: Assess
    independent_attempt <- GenerateIndependentProblem(problem_type, grade_level)
    result <- EvaluateIndependentAttempt(independent_attempt)

    // Phase 5: Remediate -- Adjust scaffold for next session
    IF result.score < mastery_threshold:
        new_scaffold <- IncreaseScaffold(scaffold_level)
        RemediateSession <- ScheduleRemediation(problem_type, new_scaffold)
    ELSE:
        FadeScaffold <- ScheduleProgression(problem_type, scaffold_depth - 1)

    RETURN ProblemSolvingRecord {
        problem: problem,
        solution_steps: solution_steps,
        scaffold_used: scaffold_level,
        assessment: result,
        next_session: FadeScaffold OR RemediateSession
    }
END FUNCTION
```

---

## Section B: Assessment Construction Templates

### Template B-1: Formative Assessment Generator

**Purpose:** Generate formative assessment items aligned to specific learning objectives with configurable cognitive level and item count, accompanied by scoring rubrics.

**Input Parameters:**
- `learning_objective` (string): The target learning objective
- `cognitive_level` (string): Bloom taxonomy level for item design
- `item_count` (integer): Number of assessment items to generate

**Output:** Item set with scoring rubric and mastery threshold

**Pseudocode:**

```
FUNCTION FormativeAssessmentGenerator(learning_objective, cognitive_level, item_count):
    // Phase 2: Select
    item_types <- SelectItemTypes(cognitive_level)
    rubric_dimensions <- ExtractRubricDimensions(learning_objective)

    // Phase 3: Deliver
    items <- EMPTY_LIST
    FOR i FROM 1 TO item_count:
        item_type <- SelectFrom(item_types)
        item <- GenerateItem(item_type, learning_objective, cognitive_level)
        item.rubric <- GenerateItemRubric(item, rubric_dimensions)
        item.discrimination_index <- EstimateDiscrimination(item)
        ADD item TO items

    // Phase 4: Assemble
    assessment <- AssembleAssessment(items)
    assessment.mastery_threshold <- CalculateMasteryThreshold(items)
    assessment.cognitive_distribution <- VerifyDistribution(items, cognitive_level)

    // Phase 5: Validate
    IF NOT PassesQualityCheck(assessment):
        RegenerateWeakItems(assessment)

    RETURN Assessment {
        items: items,
        rubric: assessment.rubric,
        mastery_threshold: assessment.mastery_threshold,
        cognitive_level: cognitive_level
    }
END FUNCTION
```

---

### Template B-2: Diagnostic Pre-Assessment

**Purpose:** Generate readiness diagnostic tests that identify prerequisite knowledge gaps before unit instruction begins, enabling targeted pre-teaching.

**Input Parameters:**
- `upcoming_unit_topics` (list): Topics to be covered in the upcoming unit
- `prerequisite_map` (object): Mapping of topics to their prerequisite knowledge items

**Output:** Readiness diagnostic with gap analysis report

**Pseudocode:**

```
FUNCTION DiagnosticPreAssessment(upcoming_unit_topics, prerequisite_map):
    // Phase 1: Diagnose (meta-diagnosis)
    all_prerequisites <- CollectPrerequisites(upcoming_unit_topics, prerequisite_map)
    knowledge_gaps <- IdentifyPotentialGaps(all_prerequisites)

    // Phase 2: Select
    diagnostic_items <- SELECT_ITEMS_FOR_GAPS(knowledge_gaps)

    // Phase 3: Deliver
    diagnostic <- AssembleDiagnostic(diagnostic_items)
    Administer(diagnostic)

    // Phase 4: Assess
    results <- CollectResults(diagnostic)
    gap_analysis <- PerformGapAnalysis(results, all_prerequisites)

    // Phase 5: Remediate (pre-teaching plan)
    IF gap_analysis.severity >= critical_threshold:
        pre_teaching_plan <- DesignPreTeaching(gap_analysis.gaps)
        RETURN DiagnosticReport {
            diagnostic: diagnostic,
            gap_analysis: gap_analysis,
            pre_teaching_plan: pre_teaching_plan,
            readiness_score: gap_analysis.readiness_score
        }
    ELSE:
        RETURN DiagnosticReport {
            diagnostic: diagnostic,
            gap_analysis: gap_analysis,
            pre_teaching_plan: NULL,
            readiness_score: gap_analysis.readiness_score,
            note: "Learners are prepared for unit instruction"
        }
    END IF
END FUNCTION
```

---

### Template B-3: Performance Task Rubric

**Purpose:** Construct analytic rubric matrices for performance-based assessments with multiple dimensions and defined performance levels.

**Input Parameters:**
- `task_description` (string): Description of the performance task
- `dimension_list` (list): List of assessment dimensions (e.g., "content_accuracy", "reasoning", "communication")
- `performance_levels` (list): Performance level labels (e.g., ["Exemplary", "Proficient", "Developing", "Beginning"])

**Output:** Analytic rubric matrix mapping dimensions to performance level descriptors

**Pseudocode:**

```
FUNCTION PerformanceTaskRubric(task_description, dimension_list, performance_levels):
    // Phase 2: Select
    level_count <- LENGTH(performance_levels)

    // Phase 3: Deliver
    rubric_matrix <- EMPTY_MATRIX[row_count=LENGTH(dimension_list), col_count=level_count]

    FOR EACH dimension IN dimension_list:
        FOR level_index FROM 0 TO level_count - 1:
            descriptor <- GenerateLevelDescriptor(
                dimension=dimension,
                level=performance_levels[level_index],
                task_description=task_description,
                level_index=level_index,
                total_levels=level_count
            )
            rubric_matrix[dimension][level_index] <- descriptor

    // Phase 4: Validate
    FOR EACH row IN rubric_matrix:
        IF NOT IsProgressive(row):
            AdjustProgression(row)
        IF NOT IsDistinct(row):
            DifferentiateDescriptors(row)

    // Phase 5: Finalize
    scoring_guide <- GenerateScoringGuide(rubric_matrix)
    student_friendly_version <- SimplifyLanguage(rubric_matrix)

    RETURN Rubric {
        task_description: task_description,
        dimensions: dimension_list,
        performance_levels: performance_levels,
        matrix: rubric_matrix,
        scoring_guide: scoring_guide,
        student_version: student_friendly_version
    }
END FUNCTION
```

---

## Section C: Classroom Management Patterns

### Template C-1: Behavior Response Ladder

**Purpose:** Provide a proportional response protocol based on behavior severity levels (1-5), ensuring consistent and escalating interventions.

**Input Parameters:**
- `behavior_severity_level` (integer): Severity rating from 1 (minor) to 5 (critical)
- `behavior_description` (string): Description of the observed behavior
- `context` (string): Classroom context (e.g., "group_work", "independent_study", "whole_class")

**Output:** Proportional response protocol with specific intervention steps

**Pseudocode:**

```
FUNCTION BehaviorResponseLadder(behavior_severity_level, behavior_description, context):
    // Validate input
    IF behavior_severity_level < 1 OR behavior_severity_level > 5:
        RETURN Error("Severity level must be between 1 and 5")

    // Phase 2: Select response protocol
    IF behavior_severity_level == 1:
        // Minor disruption -- non-verbal cue
        response <- NonVerbalIntervention(behavior_description, context)
        response.escalation_if_unsuccessful <- 2

    ELSE IF behavior_severity_level == 2:
        // Persistent minor -- verbal reminder
        response <- VerbalReminder(behavior_description, context)
        response.include_private_conversation <- true
        response.escalation_if_unsuccessful <- 3

    ELSE IF behavior_severity_level == 3:
        // Moderate -- formal conference
        response <- FormalConference(behavior_description, context)
        response.include_parent_notification <- true
        response.escalation_if_unsuccessful <- 4

    ELSE IF behavior_severity_level == 4:
        // Serious -- administrative involvement
        response <- AdministrativeIntervention(behavior_description, context)
        response.include_documentation <- true
        response.escalation_if_unsuccessful <- 5

    ELSE IF behavior_severity_level == 5:
        // Critical -- immediate safety protocol
        response <- SafetyProtocol(behavior_description, context)
        response.immediate_supervision <- true
        response.notify_administration <- true
        response.notify_parents <- true

    // Phase 4: Document
    incident_report <- GenerateIncidentReport(response)
    LogIncident(incident_report)

    // Phase 5: Follow-up
    follow_up_plan <- DesignFollowUp(response)
    ScheduleCheckIn(follow_up_plan)

    RETURN ResponseProtocol {
        severity_level: behavior_severity_level,
        intervention: response,
        incident_report: incident_report,
        follow_up_plan: follow_up_plan
    }
END FUNCTION
```

---

### Template C-2: Group Formation Algorithm

**Purpose:** Optimize group assignments based on class roster data and configurable grouping criteria to ensure balanced and productive collaborative learning.

**Input Parameters:**
- `class_roster` (list): List of student profiles with attributes (performance_level, learning_style, social_dynamics)
- `grouping_criteria` (string): Grouping strategy -- "mixed_ability", "similar_ability", "interest_based", "random"
- `group_size` (integer): Desired number of students per group

**Output:** Optimized group assignments with rationale documentation

**Pseudocode:**

```
FUNCTION GroupFormationAlgorithm(class_roster, grouping_criteria, group_size):
    // Phase 1: Diagnose
    roster_size <- LENGTH(class_roster)
    num_groups <- CEIL(roster_size / group_size)
    leftover_students <- roster_size MOD group_size

    // Phase 2: Select grouping strategy
    IF grouping_criteria == "mixed_ability":
        sorted_roster <- SortByPerformance(class_roster, descending=true)
        groups <- CreateMixedAbilityGroups(sorted_roster, num_groups, group_size)
    ELSE IF grouping_criteria == "similar_ability":
        clustered_roster <- ClusterByAbility(class_roster)
        groups <- CreateSimilarAbilityGroups(clustered_roster, num_groups, group_size)
    ELSE IF grouping_criteria == "interest_based":
        grouped_by_interest <- GroupByInterest(class_roster)
        groups <- FormInterestGroups(grouped_by_interest, num_groups, group_size)
    ELSE IF grouping_criteria == "random":
        shuffled_roster <- Shuffle(class_roster)
        groups <- PartitionIntoGroups(shuffled_roster, num_groups, group_size)

    // Phase 3: Balance check
    FOR EACH group IN groups:
        balance_score <- EvaluateGroupBalance(group)
        IF balance_score < acceptable_threshold:
            group <- RebalanceGroup(group, groups)

    // Phase 4: Document
    group_assignments <- FormatGroupAssignments(groups)
    rationale <- GenerateRationale(groups, grouping_criteria)

    // Phase 5: Output
    RETURN GroupPlan {
        groups: group_assignments,
        rationale: rationale,
        grouping_criteria: grouping_criteria,
        group_size: group_size
    }
END FUNCTION
```

---

## Section D: Curriculum Mapping Templates

### Template D-1: Unit Plan Generator

**Purpose:** Generate day-by-day unit plans aligned to curriculum standards with specified duration and thematic organization.

**Input Parameters:**
- `subject` (string): The academic subject
- `unit_theme` (string): The overarching theme or unit title
- `duration` (integer): Number of instructional days
- `standards_alignment` (list): Curriculum standards to align with

**Output:** Day-by-day unit plan with lesson objectives, activities, and assessment points

**Pseudocode:**

```
FUNCTION UnitPlanGenerator(subject, unit_theme, duration, standards_alignment):
    // Phase 1: Diagnose
    unit_scope <- DefineUnitScope(unit_theme, subject, duration)
    prerequisite_knowledge <- IdentifyPrerequisites(unit_theme, subject)

    // Phase 2: Select
    daily_breakdown <- DistributeContentOverDays(unit_scope, duration)
    assessment_points <- ScheduleAssessments(daily_breakdown, duration)

    // Phase 3: Deliver -- Day-by-day planning
    unit_plan <- EMPTY_LIST

    FOR day_index FROM 1 TO duration:
        day_content <- daily_breakdown[day_index]

        // Check if day has assessment
        IF assessment_points CONTAINS day_index:
            day_plan <- DesignAssessmentDay(day_content, standards_alignment)
        ELSE:
            day_plan <- DesignInstructionalDay(
                content=day_content,
                standards=standards_alignment,
                differentiation_options=GenerateDifferentiationOptions(day_content)
            )

        day_plan.day_number <- day_index
        day_plan.theme_connection <- LinkToUnitTheme(day_plan, unit_theme)
        ADD day_plan TO unit_plan

    // Phase 4: Validate
    IF NOT CoversAllStandards(unit_plan, standards_alignment):
        AdjustPlan(unit_plan, standards_alignment)

    // Phase 5: Finalize
    unit_plan.summary <- GenerateUnitSummary(unit_plan, unit_theme)
    unit_plan.resources <- CompileResourceList(unit_plan)

    RETURN UnitPlan {
        subject: subject,
        theme: unit_theme,
        duration: duration,
        daily_plans: unit_plan,
        standards_alignment: standards_alignment,
        resources: unit_plan.resources
    }
END FUNCTION
```

---

### Template D-2: Scope and Sequence Builder

**Purpose:** Construct term-by-term content distribution for an academic year, ensuring logical progression and standards coverage across all units.

**Input Parameters:**
- `grade_level` (integer): Target grade level
- `subject` (string): The academic subject
- `academic_year_duration` (integer): Number of terms or quarters in the academic year

**Output:** Term-by-term content distribution with pacing guide and standards mapping

**Pseudocode:**

```
FUNCTION ScopeAndSequenceBuilder(grade_level, subject, academic_year_duration):
    // Phase 1: Diagnose
    full_curriculum <- RetrieveCurriculumStandards(subject, grade_level)
    total_units <- ExtractUnits(full_curriculum)
    total_standards <- ExtractStandards(full_curriculum)

    // Phase 2: Select
    terms <- PartitionByDuration(total_units, academic_year_duration)

    // Phase 3: Deliver -- Term-by-term construction
    scope_sequence <- EMPTY_OBJECT

    FOR term_index FROM 1 TO academic_year_duration:
        term_units <- terms[term_index]

        // Calculate pacing
        term_days <- CalculateTermDays(term_index, academic_year_duration)
        pacing_guide <- DistributeDaysAcrossUnits(term_units, term_days)

        // Map standards
        term_standards <- MapStandardsToUnits(term_units, total_standards)
        coverage_gap <- IdentifyUnmappedStandards(total_standards, term_standards)

        // Build term plan
        term_plan <- {
            term: term_index,
            units: term_units,
            pacing_guide: pacing_guide,
            standards_coverage: term_standards,
            coverage_gap: coverage_gap,
            checkpoint_assessments: ScheduleTermCheckpoints(term_units)
        }

        ADD term_plan TO scope_sequence

    // Phase 4: Validate
    IF NOT CoversAllStandards(scope_sequence, total_standards):
        AdjustDistribution(scope_sequence, total_standards)

    // Phase 5: Finalize
    scope_sequence.overview <- GenerateYearOverview(scope_sequence)
    scope_sequence.gaps <- ReportRemainingGaps(scope_sequence)

    RETURN ScopeAndSequence {
        grade_level: grade_level,
        subject: subject,
        academic_year_duration: academic_year_duration,
        terms: scope_sequence,
        overview: scope_sequence.overview
    }
END FUNCTION
```

---

## Cross-Reference Index

| Template ID | Section | Purpose | Used In |
|---|---|---|---|
| A-1 | Instructional Strategy | Direct instruction delivery | SKILL.md Phase 3: Deliver |
| A-2 | Instructional Strategy | Inquiry-based learning | SKILL.md Phase 3: Deliver |
| A-3 | Instructional Strategy | Differentiated instruction | SKILL.md Phase 3: Deliver |
| A-4 | Instructional Strategy | Socratic dialogue | SKILL.md Phase 3: Deliver |
| A-5 | Instructional Strategy | Scaffolded problem-solving | SKILL.md Phase 3: Deliver |
| B-1 | Assessment Construction | Formative assessment | SKILL.md Phase 4: Assess |
| B-2 | Assessment Construction | Diagnostic pre-assessment | SKILL.md Phase 1: Diagnose |
| B-3 | Assessment Construction | Performance task rubric | SKILL.md Phase 4: Assess |
| C-1 | Classroom Management | Behavior response ladder | SKILL.md Boundary Conditions |
| C-2 | Classroom Management | Group formation algorithm | SKILL.md Phase 3: Deliver |
| D-1 | Curriculum Mapping | Unit plan generator | SKILL.md Phase 2: Select |
| D-2 | Curriculum Mapping | Scope and sequence builder | SKILL.md Phase 2: Select |

---

## Parameter Convention

All templates use the following naming conventions:
- String parameters: snake_case (e.g., `grade_level`, `learning_objective`)
- Integer parameters: snake_case (e.g., `item_count`, `scaffold_depth`)
- List parameters: plural snake_case (e.g., `dimension_list`, `upcoming_unit_topics`)
- Object parameters: camelCase (e.g., `learner_profile`, `prerequisite_map`)

All templates are parameterized -- no hardcoded values such as specific grade numbers, subject names, or curriculum content appear in the pseudocode. Every template accepts its inputs as parameters and produces structured output suitable for programmatic consumption.
