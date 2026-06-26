
// Local Business Appointment Agent
// A simple AI agent for scheduling appointments

const readline = require('readline');

// Configure business info
const business = {
  name: "Your Business Name",
  hours: {
    monday: "9:00 AM - 6:00 PM",
    tuesday: "9:00 AM - 6:00 PM",
    wednesday: "9:00 AM - 6:00 PM",
    thursday: "9:00 AM - 6:00 PM",
    friday: "9:00 AM - 6:00 PM",
    saturday: "10:00 AM - 4:00 PM",
    sunday: "Closed"
  },
  services: [
    { name: "Consultation", duration: 30, price: 50 },
    { name: "Full Service", duration: 60, price: 100 }
  ]
};

// In-memory storage for appointments (replace with a database in production)
let appointments = [];

// Set up readline for chat interface
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Main chat loop
function chat() {
  rl.question('How can I help you today? (book, cancel, reschedule, hours, services) ', (input) => {
    const command = input.toLowerCase().trim();
    
    if (command.includes('book') || command.includes('schedule')) {
      bookAppointment();
    } else if (command.includes('cancel')) {
      cancelAppointment();
    } else if (command.includes('reschedule')) {
      rescheduleAppointment();
    } else if (command.includes('hour') || command.includes('open')) {
      showHours();
    } else if (command.includes('service')) {
      showServices();
    } else {
      console.log("I can help with booking, canceling, rescheduling appointments, and showing hours/services.");
      chat();
    }
  });
}

// Book an appointment
function bookAppointment() {
  rl.question('What service would you like? ', (serviceInput) => {
    const service = business.services.find(s => s.name.toLowerCase().includes(serviceInput.toLowerCase()));
    if (!service) {
      console.log("Sorry, I don't recognize that service. Available services: " + business.services.map(s => s.name).join(', '));
      chat();
      return;
    }
    
    rl.question('What date would you like? (YYYY-MM-DD) ', (date) => {
      rl.question('What time would you like? (HH:MM AM/PM) ', (time) => {
        rl.question('What is your name? ', (name) => {
          rl.question('What is your phone number? ', (phone) => {
            const appointment = {
              id: appointments.length + 1,
              service: service.name,
              date: date,
              time: time,
              name: name,
              phone: phone
            };
            appointments.push(appointment);
            console.log(`Appointment booked! ${service.name} on ${date} at ${time} for ${name}.`);
            chat();
          });
        });
      });
    });
  });
}

// Cancel an appointment
function cancelAppointment() {
  rl.question('What is your appointment ID? ', (id) => {
    const index = appointments.findIndex(a => a.id == id);
    if (index === -1) {
      console.log("Appointment not found.");
    } else {
      appointments.splice(index, 1);
      console.log("Appointment canceled.");
    }
    chat();
  });
}

// Reschedule an appointment
function rescheduleAppointment() {
  rl.question('What is your appointment ID? ', (id) => {
    const appointment = appointments.find(a => a.id == id);
    if (!appointment) {
      console.log("Appointment not found.");
      chat();
      return;
    }
    
    rl.question('What is the new date? (YYYY-MM-DD) ', (date) => {
      rl.question('What is the new time? (HH:MM AM/PM) ', (time) => {
        appointment.date = date;
        appointment.time = time;
        console.log(`Appointment rescheduled to ${date} at ${time}.`);
        chat();
      });
    });
  });
}

// Show business hours
function showHours() {
  console.log("Business Hours:");
  for (const [day, hours] of Object.entries(business.hours)) {
    console.log(`${day.charAt(0).toUpperCase() + day.slice(1)}: ${hours}`);
  }
  chat();
}

// Show available services
function showServices() {
  console.log("Available Services:");
  business.services.forEach(service => {
    console.log(`${service.name} - ${service.duration} minutes - $${service.price}`);
  });
  chat();
}

// Start the chat
console.log(`Welcome to ${business.name}!`);
chat();
