export default {
inject:['service', 'tags'],
data(){return {
    serviceName:'',
    db:'',
    sql:'',
    cols:[],
    rows:[],
    hint:'',
    services:[]
}},
created() {
    var sl=[];
    for(var s of this.service.services) {
        sl.push(s.name);
    }
    this.serviceName=sl[0];
    this.services=sl;
},
methods:{
execute() {
    var opts={method:"POST", url:"/api/sqlexec",timeout:30000,
       data:{service:this.serviceName, db:this.db, sql:this.sql}};
    this.service.request_private(opts, "company").then(resp => {
        if(resp.code!=RetCode.OK) {
            this.hint='';
            this.$refs.errDlg.showErr(resp.code, resp.info);
            return;
        }
        
        if(resp.data.type=='SELECT') {
            this.cols = resp.data.cols;
            this.rows = resp.data.list;
        } else {
            this.cols = [];
            this.rows = [];
        }
        this.hint=this.tags.om.useTime + resp.data.time + 'ms';
    });
}
},

template: `
<q-layout view="hHh lpr fFf">
  <q-header class="bg-grey-1 text-primary">
    <q-toolbar>
      <q-btn flat round icon="arrow_back" dense @click="service.go_back"></q-btn>
      <q-toolbar-title>{{tags.om.execsqls}}</q-toolbar-title>
    </q-toolbar>
<q-list class="q-pa-sm" dense>
  <q-item>
   <q-item-section>
    <q-select v-model="serviceName" :options="services" :label="tags.om.service" outlined dense></q-select>
   </q-item-section>
   <q-item-section>
    <q-input v-model="db" :label="tags.om.db" outlined dense></q-input>
   </q-item-section>
  </q-item>
  <q-item><q-item-section>
   <q-input v-model="sql" type="textarea" outlined dense :hint="hint">
     <template v-slot:append>
      <q-icon name="play_circle_outline" @click="execute" color="primary"
       v-show="sql&&sql.length>0"></q-icon>
     </template>
   </q-input>
  </q-item-section></q-item>
</q-list>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-md">  

<q-markup-table flat>
  <thead>
   <tr><th v-for="c in cols">{{c}}</th></tr>
  </thead>
  <tbody>
  <tr v-for="row in rows">
   <td v-for="c in row">{{c}}</td>
  </tr>
  </tbody>
</q-markup-table>
    </q-page>
  </q-page-container>
</q-layout>
<component-alert-dialog :title="tags.failToCall" :close="tags.close" ref="errDlg"></component-alert-dialog>
`
}