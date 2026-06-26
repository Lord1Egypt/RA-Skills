---
name: moodle-ws
description: >
  Integrar con Moodle 4.x usando Web Services REST. Usar esta skill cuando el usuario pida
  crear cursos, inscribir o desinscribir usuarios, crear o actualizar actividades (quiz, assignment, forum),
  enviar calificaciones, listar cursos/estudiantes, o enviar mensajes internos a alumnos.
---

# Moodle Web Services (REST) – Skill

## 1. Requisitos

- URL base de Moodle (ejemplo: https://moodle.ejemplo.com)
- Token de Web Service con permisos adecuados
- Credenciales guardadas en: ~/.openclaw/workspace/secrets/moodle-ws.json

## 2. Funciones habilitadas necesarias

- core_user_get_users_by_field
- core_course_create_courses / get_courses / get_courses_by_field
- enrol_manual_enrol_users / unenrol_users
- core_enrol_get_enrolled_users
- mod_assign_create_assignments
- mod_forum_add_instance
- mod_quiz_add_instance
- core_message_send_instant_messages
- core_grades_update_grades

## 3. Ejemplos de uso natural

- "Crea un curso llamado Introducción a Python"
- "Inscribe a juan@example.com en el curso Matemáticas 1"
- "Mandales un mensaje a todos los alumnos del curso Python"
- "Mostrame todos los estudiantes del curso Inglés I"
- "Ponle un 8 a pedro@example.com en el quiz Parcial 1"

## 4. Seguridad

- Nunca mostrar el token en el chat
- Guardar URL + token fuera de Git
- Regenerar token si fue expuesto

## 5. Autoría

Skill moodle-ws diseñada por Exe Andino.
